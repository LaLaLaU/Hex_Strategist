"""测试F9热键触发
验收标准：
1.按下F9：触发截图（DEBUG_MODE=true 时保存到output/）
2.按下ESC退出监听并结束程序。
"""

from src.config import OUTPUT_DIR

def test_hotkey_capture():
    """测试按下F9触发截图"""
    from src.capture import start_capture_service

    print("="*100)
    print("热键测试启动")
    print("="*100)
    print("操作说明：")
    print("1)按下F9：触发截图")
    print(f"2)截图保存目录：{OUTPUT_DIR}")
    print("3)按ESC退出")
    print("="*100)
    print("\n等待按键...")

    start_capture_service()

if __name__ == "__main__":
    test_hotkey_capture()