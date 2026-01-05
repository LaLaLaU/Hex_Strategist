"""配置全局文件"""
import os
from dotenv import load_dotenv  #用于加载环境变量的库

load_dotenv() #加载环境变量，括号中不加环境变量时，默认读取当前工作及其父目录下的第一个.env中的配置。

#=================== 屏幕分辨率 =====================
SCREEN_RESOLUTION =  (2560,1440)

#=================== ROI区域配置 ====================
#以下配置在step1.3中写入具体设置
ROI_CONFIG = {
    "hex_name_1": (643, 550, 975, 595),  # 第一个海克斯名称位置
    "hex_name_2": (1108, 548, 1457,598),  # 第二个海克斯名称位置
    "hex_name_3": (1574, 546, 1934, 594),  # 第三个海克斯名称位置
    "hero_face":(754,1287,847,1375), # 英雄面部区域（后加）
}

#===================== API配置 =====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") #得益于load_dotenv()加载过环境变量文件.env，此处可以在.env中找到GEMINI_API_KEY，找不到就返回None
LLM_PROVIDER = os.getenv("LLM_PROVIDER","gemini")

#防御式编程，检查API的设置
# if LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
#     raise ValueError("缺少GEMINI_API_KEY请再.env文件配置")

#====================== 路径配置 ====================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT,"assets")
HEX_ICONS_DIR = os.path.join(ASSETS_DIR,"hex_icons")
OUTPUT_DIR = os.path.join(PROJECT_ROOT,"output")
LOGS_DIR = os.path.join(PROJECT_ROOT,"logs")
ROI_DIR = os.path.join(OUTPUT_DIR,"roi")

#====================== 性能配置 ====================
PHASH_THERSHOLD = 10  # phash 汉明距离阈值

#====================== 调试配置 ====================
DEBUG_MODE = True # 开启后会保存中间结果