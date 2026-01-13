"""截图模块
功能：实现全屏截图并保存为PNG文件"""


import os
import winsound
import mss
import mss.tools
import keyboard
import threading
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

def hotkey_capture_service():
    """启动截图服务：监听热键触发截图，ESC退出"""
    print("截图服务已启动：")
    def on_shot_press():
        """热键回调：执行一次截图。"""
        winsound.Beep(1200,120)
        print("\n检测到热键，开始截图...")
        filepath = capture_fullscreen()

        if filepath:
            file_size_kb = os.path.getsize(filepath) / 1024
            print(f"截图完成：{filepath}({file_size_kb:.1f}KB)")   
        else:
            print("截图完成，但DEBUFG_MODE=false,未保存文件。")

    
    keyboard.add_hotkey("ctrl+shift",on_shot_press)
    keyboard.add_hotkey("ctrl+tab",on_shot_press)
    keyboard.wait("esc")    
    print("\n已退出截图服务。") 

def capture_once_by_hotkey(capture_hotkeys=("shift+ctrl","ctrl+tab"),exit_hotkey: str = "esc"):
    """等待一次热键触发并截图，返回截图文件路径。
    - capture_hotkeys:任意一个触发键按下即截图并返回
    - exit_hotkey:按下则取消并返回 None
    """
    done = threading.Event()
    result = {"path":None}

    def _do_capture():
        # 子函数，防止连续多次导致重复触发：只响应第一次
        if done.is_set():
            return
        
        try:
            winsound.Beep(1200,120)
        except Exception:
            pass

        result["path"] = capture_fullscreen()
        done.set()

    def _do_exit():
        done.set()

    hotkey_text = " / ".join(capture_hotkeys)
    print(f"等待热键：按{hotkey_text}截图，按{exit_hotkey}取消并退出...")

    capture_handles = []
    exit_handle = None

    try:
        for hk in capture_hotkeys:
            handle = keyboard.add_hotkey(hk,_do_capture)
            capture_handles.append(handle)

        exit_handle = keyboard.add_hotkey(exit_hotkey,_do_exit)

        done.wait()
    
    finally:
    # 建立一个全量待清理列表
        all_handles = capture_handles + ([exit_handle] if exit_handle else [])
        for handle in all_handles:
            try:
                keyboard.remove_hotkey(handle)
            except Exception:
                pass # 报错说明已经释放了, 无需理会


    return result["path"]

if __name__ == "__main__":
    print("执行快速截图测试...")
    result = capture_fullscreen()
    if result:
        print(f"√ 测试成功，文件：{result}")