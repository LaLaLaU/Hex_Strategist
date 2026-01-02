"""截图模块
功能：实现全屏截图并保存为PNG文件"""


import os
import mss
import mss.tools
import mss
from datetime import datetime
from src.config import OUTPUT_DIR,DEBUG_MODE,SCREEN_RESOLUTION


def capture_fullscreen():
    """截取全屏并保存为png文件
    Returns：
        str:截图文件路径（如果DEBUG_MODE=ture）
        None：如果 DEBUG_MODE=False
    """

    # 1. 初始化 mss 截图对象
    with mss.mss() as sct:
    # 2. 获取主显示器
        monitor = sct.monitors[1]
    # 3. 截取屏幕
        screenshot = sct.grab(monitor)
    # 4. 根据DEBUG_MODE决定是否需要保存
        if DEBUG_MODE :
            # 生成带时间戳的文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.png"
            filepath = os.path.join(OUTPUT_DIR,filename)

            # 保存为png文件格式
            mss.tools.to_png(screenshot.rgb,screenshot.size,output=filepath)
            print(f"截图已保存：{filepath}")
            print(f"分辨率：{screenshot.width}x{screenshot.height}")
            return filepath
        
        else:
            print("DEBUG_MODE=false，截图未保存")
            return None

if __name__ == "__main__":
    print("执行快速截图测试...")
    result = capture_fullscreen()
    if result:
        print(f"√ 测试成功，文件：{result}")