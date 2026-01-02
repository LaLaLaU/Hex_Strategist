"""测试基本截图功能"""

import os
import time
from src.capture import capture_fullscreen
from src.config import OUTPUT_DIR

def test_capture_fullscreen():
    """测试全图截图功能"""
    print("开始测试全屏截图功能...")
    # 1.截图执行
    result = capture_fullscreen()
    # 2.等待文件写入完成
    time.sleep(0.5)
    # 3.检查OUTPUT文件夹是否有新文件
    files = os.listdir(OUTPUT_DIR)
    screenshot_files = [f for f in files if f.startswith("capture_") and f.endswith(".png")]
    screenshot_paths = [os.path.join(OUTPUT_DIR,f) for f in files if f.startswith("capture_")and f.endswith(".png")]
    # 4. 验证结果
    assert screenshot_paths ,"💔没有截图文件！"

    # 5. 检查最新截图文件
    latest_path = max(screenshot_paths,key=os.path.getmtime)
    latest_file = os.path.basename(latest_path)
    file_size = os.path.getsize(latest_path)

    print(f"👍截图文件：{latest_file}")
    print(f"👍文件大小：{file_size/1024:.2f}KB")
    print(f"👍文件路径：{latest_path}")

    print("\n🎉测试通过！")

if __name__=="__main__":
    test_capture_fullscreen()