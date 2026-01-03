"""step 1.3 ROI裁剪验证脚本
运行方式：
    python tests/test_roi.py

约定：
- 原始截图在 output/（capture_*.png）
- ROI 裁剪碎片与预览图输出到 roi/
"""

import os
from PIL import Image,ImageDraw

from src.config import OUTPUT_DIR,ROI_CONFIG,ROI_DIR

def get_latest_screenshot_path() -> str:
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("capture_") and f.endswith(".png")]

    if not files:
        raise AssertionError(
            "output/ 中没有 capture_*.png。先运行 tests/test_hotkey.py 在游戏里截一张海克斯界面。"
        )
    paths = [os.path.join(OUTPUT_DIR,f) for f in files]
    return max(paths,key=os.path.getmtime)

def validate_roi(key:str) -> tuple[int,int,int,int]:
    """检查 ROI_FONFIG[key]是否未合法的(left,top,right,bottom)。"""
    roi = ROI_CONFIG.get(key)

    if roi is None:
        raise AssertionError(f"ROI_CONFIG['{key}']未填写坐标")
    
    if not(isinstance(roi,tuple) and len(roi) == 4):
        raise AssertionError(
            f"ROI_CONFIG['{key}']必须是4元组"
        )
    
    left,top,right,bottom = roi 

    if not all(isinstance(v,int) for v in roi):
        raise AssertionError(f"ROI_CONFIG['{key}']坐标必须全是整数，现在是：{roi!r}")
    
    if right <= left or bottom <= top:
        raise AssertionError(f"ROI_CONFIG['{key}']坐标不合法：{roi!r}")
    
    return left,top,right,bottom

def  test_roi_crop():
    # 0)确保roi/目录存在
    os.makedirs(ROI_DIR,exist_ok=True)
    # 1）读取最新截图（加载图片到内存）
    screenshot_path = get_latest_screenshot_path()
    img = Image.open(screenshot_path)

    print(f"使用截图：{os.path.basename(screenshot_path)}")
    print(f"截图尺寸：{img.width}x{img.height}")
    
    # 2）当前要验证的ROI（名称框）
    keys = ["hex_name_1","hex_name_2","hex_name_3"]

    # hero_face 如果配置了也可以一起裁剪
    if ROI_CONFIG.get("hero_face") is not None:
        keys.append("hero_face")

    # 3)裁剪并保存到 roi/
    for key in keys:
        left,top,right,bottom = validate_roi(key)
        cropped = img.crop((left,top,right,bottom))
        roi_out_path = os.path.join(ROI_DIR,f"{os.path.basename(screenshot_path)}_roi_{key}.png")
        #这里os.path.basename(screenshot_path)是我自己加的，为了区分不同图片的roi
        cropped.save(roi_out_path)
        
        print(f"{key}-> {cropped.width}x{cropped.height}保存到{roi_out_path}")
    
    # 4)生成预览图（红框叠加在原图上），输出到roi/
    overlay = Image.new("RGBA",img.size,(255,255,255,0))
    draw = ImageDraw.Draw(overlay)

    for key in keys:
        left,top,right,bottom = validate_roi(key)
        draw.rectangle((left,top,right,bottom),outline=(255,0,0,255),width=3)
    
    preview = Image.alpha_composite(img.convert("RGBA"),overlay)
    preview_path = os.path.join(ROI_DIR,f"{os.path.basename(screenshot_path)}_roi_preview.png")
    preview.save(preview_path)

    print(f"\nROI 预览图：{preview_path}")
    print("手动打开它，检查红框是否准确框住ROI区域。")

if __name__ == "__main__":
    test_roi_crop()