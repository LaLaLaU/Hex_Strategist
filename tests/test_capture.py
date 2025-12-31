"""测试基本截图功能"""

import os 
import time
from src.capture import capture_fullscrenn
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
    screenshot_files = [f for f in files if f.startstwith("capture_") and f.endswith(".png")]