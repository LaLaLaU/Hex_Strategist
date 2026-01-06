"""step 1.4 - OCR 验收脚本，使用/roi里的截好的图
运行方式：
    python tests/test_ocr.py

前置条件：
-先运行 tests/test_roi.py，确保 output/roi 文件夹有 *_roi_hex_hex_name_1.png等截图文件
"""

import glob
import os

from src.config import ROI_DIR

def _latest_roi_image_path(key:str) -> str:
    pattern = os.path.join(ROI_DIR,f"*_roi_{key}.png")
    paths = glob.glob(pattern)

    if not paths:
        raise AssertionError(
        f"没有找到ROI图片：{pattern}\n"
        "请先运行：python tests/test_roi.py 生成裁剪图"
        )
    return max(paths,key=os.path.getmtime)

def test_ocr_on_hex_name_1():
    from src.ocr import recognize_text

    img_path = _latest_roi_image_path("hex_name_1")
    print(f"使用 ROI 图片：{img_path}")

    text = recognize_text(img_path)
    print(f"OCR 结果：{text!r}")

    assert isinstance(text,str)
    assert text.strip() != "", "OCR 没识别出任何文本"

if __name__ == "__main__":
    test_ocr_on_hex_name_1()