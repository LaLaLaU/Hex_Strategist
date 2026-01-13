"""step 1.5 - Phase 1 集成测试：截图 +ROI +OCR
运行方式：
python tests/test_phase1_intergration.py

通过标准（建议）：
-能生成3个 ROI 截图到 output/roi/
-OCR 至少对1个名称框识别处非空文本

"""

import os
from datetime import datetime
from PIL import Image
from src.config import ROI_CONFIG, ROI_DIR
from src.capture import capture_once_by_hotkey


def _validate_roi(key:str) -> tuple[int,int,int,int]:
    roi = ROI_CONFIG.get(key)

    if roi is None:
        raise AssertionError(f"ROI_CONFIG['{key}']未配置")
    
    if not (isinstance(roi,tuple) and len(roi) == 4 ):
        raise AssertionError(f"ROI_CONFIG['{key}']必须是4元组，现在是：{roi!r}")
    
    left,top,right,bottom = roi
    if right <= left or bottom <= top:
        raise AssertionError(f"ROI_CONFIG['{key}']坐标不合法：{roi!r}")
    
    return left,top,right,bottom

def test_phase1_integration():
    print("=" * 100)
    print("Step 1.5 - Phase 1 集成测试 （截图 + ROI + OCR）")
    print("=" * 100)


    # step 1: 截图（落地到 output/ ，返回文件路径）
    screenshot_path = capture_once_by_hotkey()
    assert screenshot_path is not None,"capture_once_by_hotkey()返回None"
    assert os.path.exists(screenshot_path),f"截图文件不存在：{screenshot_path}"

    print(f"截图路径：{screenshot_path}")

    # step 2: ROI裁剪
    os.makedirs(ROI_DIR,exist_ok=True)

    img = Image.open(screenshot_path).convert("RGB")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    roi_keys = ["hex_name_1","hex_name_2","hex_name_3"]
    roi_paths:list[tuple[str,str]] = []

    for key in roi_keys:
        left,top,right,bottom = _validate_roi(key)
        cropped = img.crop((left,top,right,bottom))

        out_name = f"{os.path.basename(screenshot_path)}_phase1_{key}_{timestamp}.png"
        out_path = os.path.join(ROI_DIR,out_name)
        cropped.save(out_path)

        roi_paths.append((key,out_path))
        print(f"{key} -> {cropped.width}x{cropped.height}保存到{out_path}")

    # step 3: OCR
    print("\n[3/3]OCR识别")

    from src.ocr import recognize_text
    non_empty = 0
    for key,path in roi_paths:
        text = recognize_text(path)
        text = (text or "").strip()
        print(f"{key} OCR:{text!r}")
        if text:
            non_empty +=1
    assert non_empty >= 1,"3个名称框OCR全为空：可能 ROI 太紧/对比度太低/需要预处理"

    print("\n ✅ Phase 1 集成测试通过")

if __name__ == "__main__":
    test_phase1_integration()