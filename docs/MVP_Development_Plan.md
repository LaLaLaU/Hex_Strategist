# Hex-Strategist MVP 开发执行计划
## 基于测试驱动开发（TDD）的原子化步骤清单

**文档性质**：固定蓝图（不修改）
**配套文档**：`Development_Log.md`（记录实际执行情况）
**开发模式**：测试驱动开发（TDD）- 先写测试，再实现功能，最后验证
**创建日期**：2025-12-27
**预计完成**：2026-02-27（60天）

---

## 🎯 TDD 核心流程（每个步骤必须遵循）

```
1. 📝 定义测试标准（这一步完成后应该看到什么）
2. 🔴 红灯：运行测试（预期失败，因为功能还没实现）
3. ✅ 绿灯：写代码实现功能（让测试通过）
4. 🔍 验证：确认测试通过
5. 📦 提交：Git commit（保存检查点）
6. ➡️ 下一步：继续下个原子步骤
```

---

## 📊 开发阶段总览

| 阶段 | 名称 | 步骤数 | 预计时间 | 核心目标 |
|-----|------|--------|---------|---------|
| **Phase 0** | 环境准备 | 8步 | 2-3天 | Python + Git + 项目结构 |
| **Phase 1** | 感知层开发 | 12步 | 7-10天 | 截图 + ROI + OCR |
| **Phase 2** | 识别层开发 | 10步 | 7-10天 | pHash + 图标匹配 |
| **Phase 3** | 决策层开发 | 8步 | 5-7天 | 知识库 + LLM API |
| **Phase 4** | 整合与测试 | 10步 | 7-10天 | 主流程 + 语音 + 实战 |

**总计**：48个原子步骤，预计30-40天（考虑学习曲线和调试时间）

---

# Phase 0: 环境准备（Pre-Development Setup）

> **目标**：配置干净的开发环境，确保所有工具可用
> **原则**：宁可多花1天配环境，也不要后面天天踩坑

---

## Step 0.1 - 安装 Python 3.10+

### 📝 测试标准（先定义期望）
- 运行 `python --version` 显示 `Python 3.10.x` 或更高版本
- 运行 `pip --version` 不报错

### 🔧 实现步骤
1. 访问 https://www.python.org/downloads/
2. 下载 **Python 3.10.11**（推荐，稳定版）
3. 安装时**勾选**：
   - ✅ Add Python to PATH（重要！）
   - ✅ Install pip
4. 安装完成后**重启终端**（PowerShell或CMD）

### ✅ 验证方法
```powershell
# 打开 PowerShell，运行以下命令
python --version
# 预期输出：Python 3.10.11

pip --version
# 预期输出：pip 23.x.x from C:\Users\...\Python310\...
```

### 🎯 通过标准
- 两条命令都不报错
- Python版本 >= 3.10

### 📦 可交付物
- 无（环境配置步骤）

### ❓ 常见问题
**Q**: 运行 `python` 提示"不是内部或外部命令"
**A**: 没勾选"Add to PATH"，重新安装或手动添加环境变量

**Q**: 显示 Python 2.7 版本
**A**: 系统有旧版本，尝试用 `python3 --version`

### 🔄 Git 提交
```bash
# 本步骤无代码，不需要提交
```

---

## Step 0.2 - 安装 Git 并配置

### 📝 测试标准
- 运行 `git --version` 显示版本号
- 运行 `git config --global user.name` 显示你的名字

### 🔧 实现步骤
1. 下载 Git for Windows: https://git-scm.com/download/win
2. 安装（全部默认选项即可）
3. 配置用户信息：
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

### ✅ 验证方法
```powershell
git --version
# 预期输出：git version 2.x.x

git config --global user.name
# 预期输出：你的名字

git config --global user.email
# 预期输出：你的邮箱
```

### 🎯 通过标准
- 三条命令都正确输出

### 📦 可交付物
- Git 全局配置完成

---

## Step 0.3 - 在 Ubuntu 服务器创建 Git 仓库

### 📝 测试标准
- 在服务器上运行 `ls ~/projects/hex-strategist.git/` 能看到 Git 仓库结构（如 `HEAD`, `config`, `objects/` 等）

### 🔧 实现步骤
1. SSH 连接到服务器：
```bash
ssh ezreau@192.168.1.200
```

2. 创建 bare 仓库：
```bash
mkdir -p ~/projects
cd ~/projects
git init --bare hex-strategist.git
```

### ✅ 验证方法
```bash
# 在服务器上运行
ls ~/projects/hex-strategist.git/
# 预期输出：branches  config  description  HEAD  hooks  info  objects  refs
```

### 🎯 通过标准
- 看到标准的 Git 仓库目录结构

### 📦 可交付物
- 服务器上的 Git bare 仓库

---

## Step 0.4 - Windows 克隆仓库并初始化项目结构

### 📝 测试标准
- 在 `e:\jiqixuexi\Hex_Strategist\` 目录下运行 `git status` 不报错
- 目录结构符合预期（包含 `src/`, `tests/`, `assets/` 等文件夹）

### 🔧 实现步骤
1. 在 Windows PowerShell 中运行：
```powershell
cd e:\jiqixuexi
git clone ezreau@192.168.1.200:~/projects/hex-strategist.git Hex_Strategist
cd Hex_Strategist
```

2. 创建项目目录结构：
```powershell
# 创建目录
New-Item -ItemType Directory -Force -Path src, tests, assets\hex_icons, assets\item_icons, output, logs

# 创建 .gitignore 文件
@"
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/

# 测试输出
output/
logs/
*.png
*.jpg
*.mp3

# IDE
.vscode/
.idea/

# 环境变量
.env
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 创建 README.md
@"
# Hex-Strategist MVP

英雄联盟海克斯大乱斗决策系统 - MVP版本

## 项目状态
🚧 开发中...

## 开发日志
详见 [Development_Log.md](Development_Log.md)
"@ | Out-File -FilePath README.md -Encoding utf8
```

### ✅ 验证方法
```powershell
# 检查目录结构
tree /F
# 预期输出：
# ├── src/
# ├── tests/
# ├── assets/
# │   ├── hex_icons/
# │   └── item_icons/
# ├── output/
# ├── logs/
# ├── .gitignore
# └── README.md

git status
# 预期输出：On branch master (或 main)
```

### 🎯 通过标准
- 目录结构完整
- `git status` 显示新文件

### 📦 可交付物
- 完整的项目目录结构
- `.gitignore` 文件
- `README.md` 文件

### 🔄 Git 提交
```bash
git add .
git commit -m "Initial project structure"
git push origin master
```

---

## Step 0.5 - 创建 Python 虚拟环境

### 📝 测试标准
- 运行 `venv\Scripts\activate` 后，命令提示符前出现 `(venv)` 标记
- 虚拟环境中运行 `python --version` 正常

### 🔧 实现步骤
```powershell
# 在项目根目录运行
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 升级 pip
python -m pip install --upgrade pip
```

### ✅ 验证方法
```powershell
# 激活后，命令提示符应该变成：
(venv) PS E:\jiqixuexi\Hex_Strategist>

# 确认 Python 路径
where python
# 预期输出：E:\jiqixuexi\Hex_Strategist\venv\Scripts\python.exe
```

### 🎯 通过标准
- 命令提示符显示 `(venv)`
- `where python` 指向虚拟环境

### 📦 可交付物
- `venv/` 目录（已在 .gitignore 中忽略）

### ❓ 常见问题
**Q**: 提示"无法加载文件...因为在此系统上禁止运行脚本"
**A**: 管理员权限运行 PowerShell，执行：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Step 0.6 - 安装基础依赖库

### 📝 测试标准（先写测试脚本）

创建 `tests/test_dependencies.py`：
```python
"""测试所有依赖库能否正常导入"""

def test_import_mss():
    """测试 mss 截图库"""
    import mss
    assert mss is not None
    print("✅ mss 导入成功")

def test_import_pillow():
    """测试 Pillow 图像处理库"""
    from PIL import Image
    assert Image is not None
    print("✅ Pillow 导入成功")

def test_import_paddleocr():
    """测试 PaddleOCR"""
    from paddleocr import PaddleOCR
    assert PaddleOCR is not None
    print("✅ PaddleOCR 导入成功")

def test_import_imagehash():
    """测试 imagehash"""
    import imagehash
    assert imagehash is not None
    print("✅ imagehash 导入成功")

def test_import_keyboard():
    """测试 keyboard 键盘监听库"""
    import keyboard
    assert keyboard is not None
    print("✅ keyboard 导入成功")

if __name__ == "__main__":
    test_import_mss()
    test_import_pillow()
    test_import_paddleocr()
    test_import_imagehash()
    test_import_keyboard()
    print("\n🎉 所有依赖库测试通过！")
```

### 🔧 实现步骤

1. **🔴 红灯**：先运行测试（应该失败）
```powershell
python tests/test_dependencies.py
# 预期输出：ModuleNotFoundError（因为还没安装）
```

2. **✅ 绿灯**：安装依赖
```powershell
# 激活虚拟环境后运行
pip install mss Pillow paddleocr imagehash keyboard

# 生成依赖清单
pip freeze > requirements.txt
```

3. **🔍 验证**：再次运行测试
```powershell
python tests/test_dependencies.py
# 预期输出：
# ✅ mss 导入成功
# ✅ Pillow 导入成功
# ✅ PaddleOCR 导入成功
# ✅ imagehash 导入成功
# ✅ keyboard 导入成功
# 🎉 所有依赖库测试通过！
```

### 🎯 通过标准
- 所有测试打印 ✅
- 最后显示 "所有依赖库测试通过！"

### 📦 可交付物
- `tests/test_dependencies.py`
- `requirements.txt`

### 🔄 Git 提交
```bash
git add tests/test_dependencies.py requirements.txt
git commit -m "Add dependency test and requirements"
git push origin master
```

### ❓ 常见问题
**Q**: PaddleOCR 安装失败
**A**: 尝试单独安装：`pip install paddleocr --no-deps`，再安装其他依赖

---

## Step 0.7 - 配置 VSCode（推荐但可选）

### 📝 测试标准
- 在 VSCode 中能正确识别虚拟环境的 Python 解释器
- 安装 Python 扩展后，代码有语法高亮和自动补全

### 🔧 实现步骤
1. 用 VSCode 打开项目：`code .`
2. 安装 Python 扩展（扩展ID: `ms-python.python`）
3. 按 `Ctrl+Shift+P`，输入 `Python: Select Interpreter`
4. 选择 `.\venv\Scripts\python.exe`

### ✅ 验证方法
- 打开 `tests/test_dependencies.py`
- 鼠标悬停在 `import mss` 上，应该显示库的文档提示
- VSCode 左下角显示：`Python 3.10.x ('venv')`

### 🎯 通过标准
- VSCode 正确识别虚拟环境

### 📦 可交付物
- 无（IDE 配置）

---

## Step 0.8 - 创建配置文件模板

### 📝 测试标准
- `src/config.py` 文件存在
- 运行 `python -c "from src.config import *; print(ROI_CONFIG)"` 能正确输出配置

### 🔧 实现步骤

创建 `src/config.py`：
```python
"""
全局配置文件
包含 ROI 坐标、API 密钥等配置项
"""

# ==================== 屏幕分辨率 ====================
SCREEN_RESOLUTION = (1920, 1080)  # 目前只支持 1920x1080

# ==================== ROI 区域配置 ====================
# 注意：坐标格式为 (left, top, right, bottom)
# 这些坐标需要在 Step 1.3 中根据实际截图标注

ROI_CONFIG = {
    "hex_choice_1": None,  # 待标注：第一个海克斯图标
    "hex_choice_2": None,  # 待标注：第二个海克斯图标
    "hex_choice_3": None,  # 待标注：第三个海克斯图标
    "hero_name": None,     # 待标注：英雄名称区域
}

# ==================== API 配置 ====================
# 在 .env 文件中配置实际的 API Key
GEMINI_API_KEY = ""  # 从环境变量读取
CLAUDE_API_KEY = ""  # 从环境变量读取

# LLM 选择（Phase 3 时决定用哪个）
LLM_PROVIDER = "gemini"  # 可选：gemini, claude, deepseek

# ==================== 路径配置 ====================
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
HEX_ICONS_DIR = os.path.join(ASSETS_DIR, "hex_icons")
ITEM_ICONS_DIR = os.path.join(ASSETS_DIR, "item_icons")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# ==================== 性能配置 ====================
SCREENSHOT_INTERVAL = 0.5  # 截图间隔（秒），MVP 阶段手动触发，暂不使用
PHASH_THRESHOLD = 10       # pHash 汉明距离阈值

# ==================== 调试配置 ====================
DEBUG_MODE = True  # 开启后会保存中间结果（截图、识别结果等）
```

### ✅ 验证方法
```powershell
# 测试配置文件能否导入
python -c "from src.config import *; print('PROJECT_ROOT:', PROJECT_ROOT); print('HEX_ICONS_DIR:', HEX_ICONS_DIR)"

# 预期输出：
# PROJECT_ROOT: E:\jiqixuexi\Hex_Strategist
# HEX_ICONS_DIR: E:\jiqixuexi\Hex_Strategist\assets\hex_icons
```

### 🎯 通过标准
- 导入成功，无报错
- 打印的路径正确

### 📦 可交付物
- `src/config.py`

### 🔄 Git 提交
```bash
git add src/config.py
git commit -m "Add config file template"
git push origin master
```

---

# Phase 1: 感知层开发（Perception Layer）

> **目标**：实现截图 + ROI 裁剪 + 基础 OCR
> **核心文件**：`src/capture.py`, `src/ocr.py`

---

## Step 1.1 - 实现基础截图功能

### 📝 测试标准（先写测试）

创建 `tests/test_capture.py`：
```python
"""测试截图功能"""
import os
from src.config import OUTPUT_DIR

def test_capture_fullscreen():
    """测试全屏截图"""
    from src.capture import capture_screen

    # 截图
    screenshot = capture_screen()

    # 断言
    assert screenshot is not None, "截图对象不应为空"
    assert screenshot.width > 0, "截图宽度应大于0"
    assert screenshot.height > 0, "截图高度应大于0"

    # 保存到 output 目录
    output_path = os.path.join(OUTPUT_DIR, "test_fullscreen.png")
    screenshot.save(output_path)

    # 验证文件存在且大小合理
    assert os.path.exists(output_path), "截图文件应该存在"
    assert os.path.getsize(output_path) > 100 * 1024, "截图文件应大于100KB"

    print(f"✅ 全屏截图成功：{output_path}")
    print(f"   尺寸：{screenshot.width}x{screenshot.height}")
    print(f"   文件大小：{os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    test_capture_fullscreen()
```

### 🔧 实现步骤

1. **🔴 红灯**：运行测试（应该失败）
```powershell
python tests/test_capture.py
# 预期输出：ModuleNotFoundError: No module named 'src.capture'
```

2. **✅ 绿灯**：实现 `src/capture.py`
```python
"""
截图模块
使用 mss 库进行高性能屏幕捕获
"""
import mss
import mss.tools
from PIL import Image
from src.config import DEBUG_MODE, OUTPUT_DIR
import os

def capture_screen(monitor_number=1):
    """
    捕获全屏截图

    Args:
        monitor_number: 显示器编号（1=主显示器）

    Returns:
        PIL.Image: 截图对象
    """
    with mss.mss() as sct:
        # 获取显示器
        monitor = sct.monitors[monitor_number]

        # 截图
        sct_img = sct.grab(monitor)

        # 转换为 PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        return img

def capture_region(region):
    """
    捕获指定区域的截图

    Args:
        region: 元组 (left, top, right, bottom)

    Returns:
        PIL.Image: 截图对象
    """
    left, top, right, bottom = region

    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top
        }

        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        return img

if __name__ == "__main__":
    # 快速测试
    print("正在截图...")
    img = capture_screen()
    print(f"截图尺寸：{img.width}x{img.height}")

    output_path = os.path.join(OUTPUT_DIR, "quick_test.png")
    img.save(output_path)
    print(f"已保存到：{output_path}")
```

3. **🔍 验证**：再次运行测试
```powershell
python tests/test_capture.py
# 预期输出：
# ✅ 全屏截图成功：E:\jiqixuexi\Hex_Strategist\output\test_fullscreen.png
#    尺寸：1920x1080
#    文件大小：xxx.x KB
```

### ✅ 额外验证
```powershell
# 手动打开生成的截图，确认能正常显示
start output\test_fullscreen.png
```

### 🎯 通过标准
- 测试脚本打印 ✅
- `output/test_fullscreen.png` 存在且大小 > 100KB
- 手动打开截图，能看到完整的屏幕内容

### 📦 可交付物
- `src/capture.py`
- `tests/test_capture.py`
- `output/test_fullscreen.png`（测试产物，不提交到 Git）

### 🔄 Git 提交
```bash
git add src/capture.py tests/test_capture.py
git commit -m "Implement basic screenshot functionality"
git push origin master
```

---

## Step 1.2 - 添加按键触发功能

### 📝 测试标准

创建 `tests/test_hotkey.py`：
```python
"""测试热键触发"""
import os
from src.config import OUTPUT_DIR

def test_hotkey_capture():
    """测试按 F9 触发截图"""
    from src.capture import start_capture_service

    print("=" * 50)
    print("🎮 热键测试启动")
    print("=" * 50)
    print("操作说明：")
    print("  1. 按 F9 键触发截图")
    print("  2. 截图会保存到 output/ 目录")
    print("  3. 按 ESC 键退出测试")
    print("=" * 50)
    print("\n等待按键...")

    # 启动监听服务
    start_capture_service()

if __name__ == "__main__":
    test_hotkey_capture()
```

### 🔧 实现步骤

1. **🔴 红灯**：运行测试
```powershell
python tests/test_hotkey.py
# 预期输出：AttributeError: module 'src.capture' has no attribute 'start_capture_service'
```

2. **✅ 绿灯**：在 `src/capture.py` 中添加热键功能
```python
# 在 src/capture.py 文件末尾添加：

import keyboard
from datetime import datetime

def start_capture_service():
    """
    启动截图服务，监听 F9 按键
    按 ESC 退出
    """
    print("截图服务已启动，监听 F9 按键...")

    def on_f9_press():
        """F9 按键回调"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)

        print(f"\n📸 正在截图...")
        img = capture_screen()
        img.save(output_path)

        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ 截图已保存：{filename} ({file_size:.1f} KB)")

    # 注册热键
    keyboard.add_hotkey('f9', on_f9_press)

    # 等待 ESC 退出
    print("按 ESC 键退出...")
    keyboard.wait('esc')

    print("\n截图服务已停止")
```

3. **🔍 验证**：运行测试并手动操作
```powershell
python tests/test_hotkey.py
# 然后：
# 1. 按 F9，观察是否打印 "✅ 截图已保存"
# 2. 检查 output/ 目录是否生成新截图
# 3. 按 ESC 退出
```

### 🎯 通过标准
- 按 F9 后，控制台打印 ✅ 消息
- `output/capture_YYYYMMDD_HHMMSS.png` 文件生成
- 按 ESC 能正常退出

### 📦 可交付物
- 更新的 `src/capture.py`
- `tests/test_hotkey.py`

### 🔄 Git 提交
```bash
git add src/capture.py tests/test_hotkey.py
git commit -m "Add hotkey trigger (F9) for screenshot"
git push origin master
```

---

## Step 1.3 - 标注 ROI 区域坐标

### 📝 测试标准
- 进入游戏，按 F9 截取海克斯选择界面
- 使用标注工具记录3个图标的精确坐标
- 更新 `src/config.py` 中的 `ROI_CONFIG`
- 运行验证脚本，能正确裁剪出3个图标

### 🔧 实现步骤

**🎮 游戏内操作（需要你亲自做）：**

1. 启动《英雄联盟》，进入"海克斯大乱斗"模式
2. 运行热键服务：
```powershell
python tests/test_hotkey.py
```
3. 在游戏中触发海克斯选择界面（Level 3/7/11/15）
4. **立即按 F9** 截图
5. 按 ESC 退出服务
6. 找到 `output/` 目录中最新的截图

**🖼️ 标注坐标（Windows 画图工具）：**

1. 右键截图 → 打开方式 → 画图
2. 用鼠标在图标上移动，**记录左下角显示的坐标**
3. 记录每个图标的：
   - 左上角坐标 `(left, top)`
   - 右下角坐标 `(right, bottom)`

**示例**（仅供参考，实际需测量）：
```
图标1：left=600,  top=400,  right=680,  bottom=480
图标2：left=850,  top=400,  right=930,  bottom=480
图标3：left=1100, top=400,  right=1180, bottom=480
```

**📝 创建测试脚本** `tests/test_roi.py`：
```python
"""测试 ROI 裁剪"""
import os
from PIL import Image, ImageDraw
from src.config import OUTPUT_DIR, ROI_CONFIG

def test_roi_crop():
    """测试 ROI 区域裁剪"""
    # 读取最新的截图
    screenshots = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith("capture_")])
    if not screenshots:
        print("❌ 没有找到截图，请先运行 test_hotkey.py 并按 F9 截图")
        return

    latest = os.path.join(OUTPUT_DIR, screenshots[-1])
    img = Image.open(latest)
    print(f"📸 使用截图：{screenshots[-1]}")

    # 检查 ROI 是否已配置
    if ROI_CONFIG["hex_choice_1"] is None:
        print("❌ ROI 坐标未配置，请先在 src/config.py 中填写坐标")
        return

    # 裁剪并保存3个图标
    for i in [1, 2, 3]:
        key = f"hex_choice_{i}"
        roi = ROI_CONFIG[key]

        if roi is None:
            print(f"⚠️ {key} 未配置")
            continue

        left, top, right, bottom = roi
        cropped = img.crop((left, top, right, bottom))

        output_path = os.path.join(OUTPUT_DIR, f"roi_test_icon_{i}.png")
        cropped.save(output_path)

        print(f"✅ 图标{i} 裁剪成功：{cropped.width}x{cropped.height}")
        print(f"   保存到：{output_path}")

    # 绘制 ROI 框在原图上
    draw = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw_obj = ImageDraw.Draw(draw)

    for i in [1, 2, 3]:
        roi = ROI_CONFIG[f"hex_choice_{i}"]
        if roi:
            draw_obj.rectangle(roi, outline=(255, 0, 0, 255), width=3)

    combined = Image.alpha_composite(img.convert('RGBA'), draw)
    preview_path = os.path.join(OUTPUT_DIR, "roi_preview.png")
    combined.save(preview_path)

    print(f"\n📊 ROI 预览图已生成：{preview_path}")
    print("   手动打开查看红框是否准确框住图标")

if __name__ == "__main__":
    test_roi_crop()
```

**✏️ 更新配置文件** `src/config.py`：
```python
# 根据你的实际测量结果填写
ROI_CONFIG = {
    # ⚠️ 这里的坐标需要你自己测量后填写！
    # 示例（1920x1080分辨率）：
    "hex_choice_1": (600, 400, 680, 480),   # 第一个海克斯图标
    "hex_choice_2": (850, 400, 930, 480),   # 第二个海克斯图标
    "hex_choice_3": (1100, 400, 1180, 480), # 第三个海克斯图标
    "hero_name": (50, 50, 300, 100),        # 英雄名称区域（暂不使用）
}
```

### ✅ 验证方法
```powershell
# 运行 ROI 测试
python tests/test_roi.py

# 预期输出：
# 📸 使用截图：capture_20250127_143022.png
# ✅ 图标1 裁剪成功：80x80
#    保存到：...
# ✅ 图标2 裁剪成功：80x80
# ✅ 图标3 裁剪成功：80x80
# 📊 ROI 预览图已生成：...

# 手动打开查看
start output\roi_preview.png
# 检查红框是否准确框住3个图标
```

### 🎯 通过标准
- 生成3个裁剪图标（`roi_test_icon_1/2/3.png`）
- 每个图标是清晰的 80x80 左右的图像
- `roi_preview.png` 中的红框准确框住3个图标

### 📦 可交付物
- 更新的 `src/config.py`（包含实际坐标）
- `tests/test_roi.py`
- `output/roi_preview.png`（验证产物）

### 🔄 Git 提交
```bash
git add src/config.py tests/test_roi.py
git commit -m "Add ROI configuration and test"
git push origin master
```

### ❓ 常见问题
**Q**: 坐标不准确，裁剪出来的图标偏了
**A**: 用画图工具重新测量，注意左上角和右下角坐标不要搞反

**Q**: 不同分辨率怎么办？
**A**: MVP 阶段只支持 1920x1080，其他分辨率需要重新标注

---

## Step 1.4 - 实现 OCR 文本识别

### 📝 测试标准（先写测试）

创建 `tests/test_ocr.py`：
```python
"""测试 OCR 识别"""
import os
from PIL import Image, ImageDraw, ImageFont
from src.config import OUTPUT_DIR

def create_test_image():
    """创建一个包含文本的测试图片"""
    img = Image.new('RGB', (400, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 写一些文本
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    draw.text((20, 30), "Test OCR 1234", fill=(0, 0, 0), font=font)

    test_img_path = os.path.join(OUTPUT_DIR, "test_ocr_input.png")
    img.save(test_img_path)
    return test_img_path

def test_ocr_basic():
    """测试基础 OCR 功能"""
    from src.ocr import recognize_text

    # 创建测试图片
    test_img_path = create_test_image()
    print(f"📸 测试图片已创建：{test_img_path}")

    # 识别
    print("\n开始 OCR 识别...")
    result = recognize_text(test_img_path)

    print("\n识别结果：")
    print(result)

    # 检查是否包含关键字
    result_lower = result.lower()
    assert "test" in result_lower or "ocr" in result_lower, \
        "应该识别出 'test' 或 'ocr' 关键词"

    print("\n✅ OCR 测试通过！")

if __name__ == "__main__":
    test_ocr_basic()
```

### 🔧 实现步骤

1. **🔴 红灯**：运行测试
```powershell
python tests/test_ocr.py
# 预期：ModuleNotFoundError: No module named 'src.ocr'
```

2. **✅ 绿灯**：实现 `src/ocr.py`
```python
"""
OCR 模块
使用 PaddleOCR 进行文本识别
"""
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# 初始化 OCR（只初始化一次，提高性能）
# use_angle_cls=True：支持文字旋转识别
# lang='ch'：中文+英文
_ocr_instance = None

def get_ocr_instance():
    """获取 OCR 单例"""
    global _ocr_instance
    if _ocr_instance is None:
        print("🔧 初始化 PaddleOCR（首次使用会下载模型，需要一点时间）...")
        _ocr_instance = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            show_log=False  # 关闭详细日志
        )
    return _ocr_instance

def recognize_text(image_path_or_array):
    """
    识别图像中的文本

    Args:
        image_path_or_array: 图片路径（str）或 PIL.Image 或 numpy.ndarray

    Returns:
        str: 识别出的文本（多行用空格连接）
    """
    ocr = get_ocr_instance()

    # 统一转换为 numpy array
    if isinstance(image_path_or_array, str):
        img = Image.open(image_path_or_array)
        img_array = np.array(img)
    elif isinstance(image_path_or_array, Image.Image):
        img_array = np.array(image_path_or_array)
    else:
        img_array = image_path_or_array

    # 执行 OCR
    result = ocr.ocr(img_array, cls=True)

    # 解析结果
    if result is None or len(result) == 0 or result[0] is None:
        return ""

    # 提取文本
    texts = []
    for line in result[0]:
        if line[1][0]:  # line[1][0] 是识别出的文本
            texts.append(line[1][0])

    return " ".join(texts)

if __name__ == "__main__":
    # 快速测试
    print("OCR 模块加载成功")
    print("运行 tests/test_ocr.py 进行完整测试")
```

3. **🔍 验证**：运行测试
```powershell
python tests/test_ocr.py

# 预期输出（首次运行会下载模型）：
# 🔧 初始化 PaddleOCR（首次使用会下载模型，需要一点时间）...
# 📸 测试图片已创建：...
# 开始 OCR 识别...
# 识别结果：
# Test OCR 1234
# ✅ OCR 测试通过！
```

### 🎯 通过标准
- 测试打印 ✅
- 识别结果包含 "test" 或 "ocr" 关键词

### 📦 可交付物
- `src/ocr.py`
- `tests/test_ocr.py`

### 🔄 Git 提交
```bash
git add src/ocr.py tests/test_ocr.py
git commit -m "Implement OCR functionality with PaddleOCR"
git push origin master
```

### ❓ 常见问题
**Q**: 下载模型失败
**A**: 检查网络连接，或手动下载模型后放到 `~/.paddleocr/` 目录

**Q**: 识别准确率低
**A**: MVP 阶段可接受，后续可调整图片预处理（二值化、去噪）

---

## Step 1.5 - Phase 1 集成测试

### 📝 测试标准

创建 `tests/test_phase1_integration.py`：
```python
"""Phase 1 集成测试：截图 + ROI + OCR"""
import os
from src.capture import capture_screen
from src.config import OUTPUT_DIR, ROI_CONFIG
from datetime import datetime

def test_full_capture_pipeline():
    """测试完整的感知层流程"""
    print("=" * 60)
    print("Phase 1 集成测试")
    print("=" * 60)

    # Step 1: 截图
    print("\n📸 Step 1: 全屏截图...")
    screenshot = capture_screen()
    assert screenshot is not None
    print(f"✅ 截图成功：{screenshot.width}x{screenshot.height}")

    # Step 2: ROI 裁剪
    print("\n✂️ Step 2: ROI 裁剪...")
    cropped_icons = []
    for i in [1, 2, 3]:
        roi = ROI_CONFIG[f"hex_choice_{i}"]
        if roi is None:
            print(f"⚠️ hex_choice_{i} 未配置，跳过")
            continue

        icon = screenshot.crop(roi)
        cropped_icons.append((i, icon))
        print(f"✅ 图标{i} 裁剪成功：{icon.width}x{icon.height}")

    assert len(cropped_icons) > 0, "至少应该裁剪出1个图标"

    # Step 3: 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for idx, icon in cropped_icons:
        filename = f"phase1_test_icon_{idx}_{timestamp}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)
        icon.save(output_path)
        print(f"💾 已保存：{filename}")

    print("\n" + "=" * 60)
    print("🎉 Phase 1 集成测试通过！")
    print("=" * 60)
    print("\n✅ 感知层功能正常：")
    print("   - 截图功能 ✓")
    print("   - ROI 裁剪 ✓")
    print("   - 文件保存 ✓")
    print("\n下一步：开始 Phase 2（识别层开发）")

if __name__ == "__main__":
    test_full_capture_pipeline()
```

### ✅ 验证方法
```powershell
python tests/test_phase1_integration.py

# 预期输出：
# ==================================================
# Phase 1 集成测试
# ==================================================
#
# 📸 Step 1: 全屏截图...
# ✅ 截图成功：1920x1080
#
# ✂️ Step 2: ROI 裁剪...
# ✅ 图标1 裁剪成功：80x80
# ✅ 图标2 裁剪成功：80x80
# ✅ 图标3 裁剪成功：80x80
# 💾 已保存：phase1_test_icon_1_20250127_150030.png
# ...
#
# 🎉 Phase 1 集成测试通过！
```

### 🎯 通过标准
- 所有步骤打印 ✅
- 生成 3 个测试图标文件

### 📦 可交付物
- `tests/test_phase1_integration.py`

### 🔄 Git 提交
```bash
git add tests/test_phase1_integration.py
git commit -m "Add Phase 1 integration test"
git push origin master
```

---

# Phase 2: 识别层开发（Recognition Layer）

> **目标**：实现 pHash 图标识别
> **核心文件**：`src/recognition.py`

---

## Step 2.1 - 收集海克斯图标素材

### 📝 测试标准
- `assets/hex_icons/` 目录下至少有 10 个图标文件
- 每个文件命名规范：`{hex_id}.png`（如 `cybernetic_shell.png`）
- 创建 `assets/hex_icons/index.json` 记录图标元数据

### 🔧 实现步骤

**📥 图标下载（手动操作）：**

1. 访问英雄联盟 Wiki：
   - https://leagueoflegends.fandom.com/wiki/Arena_(League_of_Legends)
   - 或搜索 "海克斯大乱斗强化"

2. 下载常见海克斯图标（优先选择高频出现的）：
   - 建议先下载 10-15 个常见的
   - 保存到 `assets/hex_icons/` 目录
   - 命名格式：`augment_name.png`（使用英文名或拼音）

**示例（你需要自己下载实际图标）：**
```
assets/hex_icons/
├── cybernetic_shell.png        # 义体外壳
├── berserker_rage.png           # 狂战士之怒
├── regeneration_aura.png        # 再生光环
├── infinity_force.png           # 无尽之力
├── (更多...)
```

**📝 创建索引文件** `assets/hex_icons/index.json`：
```json
{
  "cybernetic_shell": {
    "name_zh": "义体外壳",
    "name_en": "Cybernetic Shell",
    "description": "受到伤害时获得护盾"
  },
  "berserker_rage": {
    "name_zh": "狂战士之怒",
    "name_en": "Berserker Rage",
    "description": "攻击速度大幅提升"
  },
  "regeneration_aura": {
    "name_zh": "再生光环",
    "name_en": "Regeneration Aura",
    "description": "持续恢复生命值"
  }
}
```

**🔍 创建验证脚本** `tests/test_assets.py`：
```python
"""测试图标素材完整性"""
import os
import json
from PIL import Image
from src.config import HEX_ICONS_DIR, ASSETS_DIR

def test_hex_icons():
    """测试海克斯图标素材"""
    index_path = os.path.join(HEX_ICONS_DIR, "index.json")

    # 检查 index.json 是否存在
    assert os.path.exists(index_path), f"缺少索引文件：{index_path}"

    # 加载索引
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    print(f"📂 图标库索引：{len(index)} 个强化")

    # 验证每个图标
    for hex_id, meta in index.items():
        icon_path = os.path.join(HEX_ICONS_DIR, f"{hex_id}.png")

        assert os.path.exists(icon_path), f"缺少图标文件：{icon_path}"

        # 检查图片能否打开
        img = Image.open(icon_path)
        print(f"✅ {hex_id:25s} ({meta['name_zh']:10s}) - {img.width}x{img.height}")

    print(f"\n🎉 图标素材验证通过！共 {len(index)} 个图标")
    return len(index)

if __name__ == "__main__":
    count = test_hex_icons()
    if count < 10:
        print(f"\n⚠️ 当前只有 {count} 个图标，建议收集至少 10 个")
```

### ✅ 验证方法
```powershell
python tests/test_assets.py

# 预期输出：
# 📂 图标库索引：10 个强化
# ✅ cybernetic_shell       (义体外壳    ) - 80x80
# ✅ berserker_rage         (狂战士之怒  ) - 80x80
# ...
# 🎉 图标素材验证通过！共 10 个图标
```

### 🎯 通过标准
- 至少 10 个图标文件存在
- `index.json` 正确加载
- 所有图标能正常打开

### 📦 可交付物
- `assets/hex_icons/*.png`（至少10个）
- `assets/hex_icons/index.json`
- `tests/test_assets.py`

### 🔄 Git 提交
```bash
git add assets/hex_icons/ tests/test_assets.py
git commit -m "Add hex icon assets and validation test"
git push origin master
```

### ❓ 常见问题
**Q**: 去哪里下载图标？
**A**: Wiki、游戏官网、或者进游戏自己截图裁剪

**Q**: 图标大小不一致怎么办？
**A**: 可以用 Pillow 统一调整大小（建议 64x64 或 80x80）

---

## Step 2.2 - 实现 pHash 指纹计算

### 📝 测试标准（先写测试）

创建 `tests/test_phash.py`：
```python
"""测试 pHash 指纹计算"""
import os
from PIL import Image
from src.config import HEX_ICONS_DIR, OUTPUT_DIR

def test_phash_calculation():
    """测试计算图标的 pHash 指纹"""
    from src.recognition import calculate_phash

    # 随便选一个图标
    icons = [f for f in os.listdir(HEX_ICONS_DIR) if f.endswith('.png') and f != 'index.json']
    if not icons:
        print("❌ 没有找到图标文件，请先完成 Step 2.1")
        return

    test_icon = os.path.join(HEX_ICONS_DIR, icons[0])
    print(f"测试图标：{icons[0]}")

    # 计算 pHash
    hash1 = calculate_phash(test_icon)
    print(f"pHash 指纹：{hash1}")

    # 同一张图片应该得到相同的哈希
    hash2 = calculate_phash(test_icon)
    assert hash1 == hash2, "同一张图片的 pHash 应该相同"

    # 计算汉明距离（应该为0）
    distance = hash1 - hash2
    assert distance == 0, "同一张图片的汉明距离应该为0"

    print(f"✅ pHash 计算正确，汉明距离 = {distance}")

def test_phash_similarity():
    """测试 pHash 相似度检测"""
    from src.recognition import calculate_phash
    from PIL import Image, ImageEnhance

    # 选一个图标
    icons = [f for f in os.listdir(HEX_ICONS_DIR) if f.endswith('.png')]
    if len(icons) < 2:
        print("⚠️ 图标少于2个，跳过相似度测试")
        return

    icon1_path = os.path.join(HEX_ICONS_DIR, icons[0])
    icon2_path = os.path.join(HEX_ICONS_DIR, icons[1])

    hash1 = calculate_phash(icon1_path)
    hash2 = calculate_phash(icon2_path)

    distance_diff = hash1 - hash2
    print(f"\n不同图标的汉明距离：{distance_diff}")

    # 创建一个稍微变化的图片（调整亮度）
    img = Image.open(icon1_path)
    enhancer = ImageEnhance.Brightness(img)
    img_bright = enhancer.enhance(1.2)  # 亮度 +20%

    temp_path = os.path.join(OUTPUT_DIR, "temp_bright.png")
    img_bright.save(temp_path)

    hash_bright = calculate_phash(temp_path)
    distance_similar = hash1 - hash_bright

    print(f"相似图片的汉明距离：{distance_similar}")

    # 相似图片的距离应该很小
    assert distance_similar < 10, "相似图片的汉明距离应该 < 10"

    print(f"✅ pHash 相似度检测正常")

if __name__ == "__main__":
    print("=" * 50)
    print("pHash 测试")
    print("=" * 50)
    test_phash_calculation()
    test_phash_similarity()
    print("\n🎉 所有 pHash 测试通过！")
```

### 🔧 实现步骤

1. **🔴 红灯**：运行测试
```powershell
python tests/test_phash.py
# 预期：ModuleNotFoundError
```

2. **✅ 绿灯**：实现 `src/recognition.py`
```python
"""
识别模块
使用 pHash 进行图标识别
"""
import os
import json
import imagehash
from PIL import Image
from src.config import HEX_ICONS_DIR, PHASH_THRESHOLD

def calculate_phash(image_path_or_pil, hash_size=8):
    """
    计算图片的 pHash 指纹

    Args:
        image_path_or_pil: 图片路径或 PIL.Image 对象
        hash_size: 哈希大小（默认8，生成64位哈希）

    Returns:
        imagehash.ImageHash: pHash 对象
    """
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil)
    else:
        img = image_path_or_pil

    return imagehash.phash(img, hash_size=hash_size)

def load_hex_icon_database():
    """
    加载海克斯图标数据库

    Returns:
        dict: {hex_id: {"hash": pHash对象, "meta": 元数据}}
    """
    database = {}

    # 加载 index.json
    index_path = os.path.join(HEX_ICONS_DIR, "index.json")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"缺少索引文件：{index_path}")

    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    # 计算每个图标的 pHash
    for hex_id in index.keys():
        icon_path = os.path.join(HEX_ICONS_DIR, f"{hex_id}.png")
        if not os.path.exists(icon_path):
            print(f"⚠️ 图标文件不存在：{icon_path}")
            continue

        phash = calculate_phash(icon_path)
        database[hex_id] = {
            "hash": phash,
            "meta": index[hex_id]
        }

    return database

# 全局缓存（避免重复加载）
_icon_database = None

def get_icon_database():
    """获取图标数据库单例"""
    global _icon_database
    if _icon_database is None:
        _icon_database = load_hex_icon_database()
        print(f"📚 图标数据库已加载：{len(_icon_database)} 个强化")
    return _icon_database

if __name__ == "__main__":
    # 快速测试
    db = get_icon_database()
    for hex_id, data in list(db.items())[:3]:
        print(f"{hex_id}: {data['hash']}")
```

3. **🔍 验证**：运行测试
```powershell
python tests/test_phash.py

# 预期输出：
# ==================================================
# pHash 测试
# ==================================================
# 测试图标：cybernetic_shell.png
# pHash 指纹：1a2b3c4d5e6f7g8h
# ✅ pHash 计算正确，汉明距离 = 0
#
# 不同图标的汉明距离：25
# 相似图片的汉明距离：3
# ✅ pHash 相似度检测正常
#
# 🎉 所有 pHash 测试通过！
```

### 🎯 通过标准
- 所有测试打印 ✅
- 相似图片的汉明距离 < 10

### 📦 可交付物
- `src/recognition.py`
- `tests/test_phash.py`

### 🔄 Git 提交
```bash
git add src/recognition.py tests/test_phash.py
git commit -m "Implement pHash calculation and icon database"
git push origin master
```

---

## Step 2.3 - 实现图标匹配功能

### 📝 测试标准（先写测试）

创建 `tests/test_matching.py`：
```python
"""测试图标匹配功能"""
import os
from PIL import Image
from src.config import HEX_ICONS_DIR, OUTPUT_DIR

def test_match_exact():
    """测试精确匹配（使用库中的原图）"""
    from src.recognition import match_icon, get_icon_database

    # 随便选一个图标
    db = get_icon_database()
    test_hex_id = list(db.keys())[0]
    test_icon_path = os.path.join(HEX_ICONS_DIR, f"{test_hex_id}.png")

    print(f"测试图标：{test_hex_id}")

    # 匹配
    result = match_icon(test_icon_path)

    print(f"匹配结果：{result['hex_id']} ({result['name_zh']})")
    print(f"汉明距离：{result['distance']}")
    print(f"置信度：{result['confidence']:.2%}")

    # 精确匹配应该距离为0
    assert result['hex_id'] == test_hex_id, "应该匹配到原图标"
    assert result['distance'] == 0, "精确匹配距离应为0"

    print("✅ 精确匹配测试通过")

def test_match_similar():
    """测试相似匹配（稍微修改的图片）"""
    from src.recognition import match_icon
    from PIL import ImageEnhance

    # 选一个图标并修改亮度
    icons = [f for f in os.listdir(HEX_ICONS_DIR) if f.endswith('.png')]
    original_path = os.path.join(HEX_ICONS_DIR, icons[0])

    img = Image.open(original_path)
    enhancer = ImageEnhance.Brightness(img)
    img_modified = enhancer.enhance(1.3)

    temp_path = os.path.join(OUTPUT_DIR, "test_match_similar.png")
    img_modified.save(temp_path)

    print(f"\n测试图标（亮度+30%）：{icons[0]}")

    # 匹配
    result = match_icon(temp_path)

    print(f"匹配结果：{result['hex_id']} ({result['name_zh']})")
    print(f"汉明距离：{result['distance']}")
    print(f"置信度：{result['confidence']:.2%}")

    # 应该还能匹配到原图标
    expected_id = icons[0].replace('.png', '')
    assert result['hex_id'] == expected_id, "应该匹配到原图标"
    assert result['distance'] < 10, "相似匹配距离应 < 10"

    print("✅ 相似匹配测试通过")

if __name__ == "__main__":
    print("=" * 50)
    print("图标匹配测试")
    print("=" * 50)
    test_match_exact()
    test_match_similar()
    print("\n🎉 所有匹配测试通过！")
```

### 🔧 实现步骤

1. **🔴 红灯**：运行测试
```powershell
python tests/test_matching.py
# 预期：AttributeError: 'module' has no attribute 'match_icon'
```

2. **✅ 绿灯**：在 `src/recognition.py` 中添加匹配功能
```python
# 在 src/recognition.py 中添加：

def match_icon(image_path_or_pil, threshold=None):
    """
    匹配图标

    Args:
        image_path_or_pil: 待匹配的图片
        threshold: 汉明距离阈值（默认使用配置文件中的值）

    Returns:
        dict: {
            "hex_id": str,        # 匹配到的ID
            "name_zh": str,       # 中文名
            "name_en": str,       # 英文名
            "distance": int,      # 汉明距离
            "confidence": float   # 置信度 (0-1)
        }
        如果没有匹配到，返回 None
    """
    if threshold is None:
        threshold = PHASH_THRESHOLD

    # 计算待匹配图片的 pHash
    query_hash = calculate_phash(image_path_or_pil)

    # 加载数据库
    db = get_icon_database()

    # 遍历所有图标，找到最相似的
    best_match = None
    min_distance = float('inf')

    for hex_id, data in db.items():
        distance = query_hash - data['hash']  # 汉明距离

        if distance < min_distance:
            min_distance = distance
            best_match = {
                "hex_id": hex_id,
                "name_zh": data['meta']['name_zh'],
                "name_en": data['meta']['name_en'],
                "distance": distance,
                "confidence": max(0, 1 - distance / 64)  # 简单的置信度计算
            }

    # 检查是否超过阈值
    if best_match and best_match['distance'] <= threshold:
        return best_match
    else:
        return None

def match_three_icons(icon1, icon2, icon3):
    """
    匹配三个图标（海克斯三选一场景）

    Args:
        icon1, icon2, icon3: PIL.Image 对象或图片路径

    Returns:
        list: 三个匹配结果的列表
    """
    results = []
    for i, icon in enumerate([icon1, icon2, icon3], 1):
        result = match_icon(icon)
        if result:
            result['position'] = i  # 添加位置信息（第几个选项）
            results.append(result)
        else:
            results.append({
                "position": i,
                "hex_id": "unknown",
                "name_zh": "未识别",
                "distance": 999,
                "confidence": 0
            })

    return results
```

3. **🔍 验证**：运行测试
```powershell
python tests/test_matching.py

# 预期输出：
# ==================================================
# 图标匹配测试
# ==================================================
# 📚 图标数据库已加载：10 个强化
# 测试图标：cybernetic_shell
# 匹配结果：cybernetic_shell (义体外壳)
# 汉明距离：0
# 置信度：100.00%
# ✅ 精确匹配测试通过
#
# 测试图标（亮度+30%）：cybernetic_shell.png
# 匹配结果：cybernetic_shell (义体外壳)
# 汉明距离：2
# 置信度：96.88%
# ✅ 相似匹配测试通过
#
# 🎉 所有匹配测试通过！
```

### 🎯 通过标准
- 精确匹配距离 = 0
- 相似匹配距离 < 10
- 所有测试打印 ✅

### 📦 可交付物
- 更新的 `src/recognition.py`
- `tests/test_matching.py`

### 🔄 Git 提交
```bash
git add src/recognition.py tests/test_matching.py
git commit -m "Implement icon matching with pHash"
git push origin master
```

---

## Step 2.4 - Phase 2 集成测试（游戏内真实测试）

### 📝 测试标准
- 进入游戏，截取海克斯选择界面
- 裁剪3个图标
- 识别出至少2个图标的正确名称

### 🔧 实现步骤

创建 `tests/test_phase2_integration.py`：
```python
"""Phase 2 集成测试：完整识别流程"""
import os
from src.capture import capture_screen
from src.config import OUTPUT_DIR, ROI_CONFIG
from src.recognition import match_three_icons
from datetime import datetime

def test_full_recognition_pipeline():
    """
    测试完整识别流程

    操作步骤：
    1. 进入游戏，触发海克斯选择界面
    2. 按 F9 截图（使用 test_hotkey.py）
    3. 运行本测试脚本
    """
    print("=" * 60)
    print("Phase 2 集成测试：游戏内真实识别")
    print("=" * 60)

    # 使用最新的截图
    screenshots = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith("capture_")])
    if not screenshots:
        print("❌ 没有找到截图，请先运行 test_hotkey.py 并按 F9")
        print("   或者运行 python -c \"from src.capture import start_capture_service; start_capture_service()\"")
        return

    latest = os.path.join(OUTPUT_DIR, screenshots[-1])
    img = Image.open(latest)
    print(f"📸 使用截图：{screenshots[-1]}")

    # 裁剪3个图标
    icons = []
    for i in [1, 2, 3]:
        roi = ROI_CONFIG[f"hex_choice_{i}"]
        if roi is None:
            print(f"⚠️ hex_choice_{i} 未配置")
            continue

        icon = img.crop(roi)
        icons.append(icon)

        # 保存裁剪的图标（调试用）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_path = os.path.join(OUTPUT_DIR, f"phase2_icon_{i}_{timestamp}.png")
        icon.save(debug_path)

    if len(icons) < 3:
        print("❌ ROI 配置不完整，请检查 src/config.py")
        return

    # 识别
    print("\n🔍 开始识别...")
    results = match_three_icons(icons[0], icons[1], icons[2])

    print("\n识别结果：")
    print("-" * 60)
    success_count = 0
    for result in results:
        status = "✅" if result['hex_id'] != "unknown" else "❌"
        print(f"{status} 选项{result['position']}: {result['name_zh']} ({result['hex_id']})")
        print(f"   汉明距离: {result['distance']}, 置信度: {result['confidence']:.2%}")

        if result['hex_id'] != "unknown":
            success_count += 1

    print("-" * 60)
    print(f"\n识别成功率：{success_count}/3 = {success_count/3:.1%}")

    if success_count >= 2:
        print("\n🎉 Phase 2 集成测试通过！")
        print("\n✅ 识别层功能正常：")
        print("   - pHash 计算 ✓")
        print("   - 图标匹配 ✓")
        print("   - 游戏内识别 ✓")
        print("\n下一步：开始 Phase 3（决策层开发）")
    else:
        print("\n⚠️ 识别率偏低，可能的原因：")
        print("   1. ROI 坐标不准确（重新标注）")
        print("   2. 图标库不完整（添加更多图标）")
        print("   3. 图标质量问题（重新下载高清图标）")

if __name__ == "__main__":
    from PIL import Image
    test_full_recognition_pipeline()
```

### ✅ 验证方法（需要游戏内操作）

```powershell
# Step 1: 进入游戏，触发海克斯选择界面

# Step 2: 截图
python tests/test_hotkey.py
# 按 F9 截图，然后按 ESC 退出

# Step 3: 运行识别测试
python tests/test_phase2_integration.py

# 预期输出：
# 📸 使用截图：capture_20250127_160530.png
# 🔍 开始识别...
#
# 识别结果：
# ------------------------------------------------------------
# ✅ 选项1: 义体外壳 (cybernetic_shell)
#    汉明距离: 3, 置信度: 95.31%
# ✅ 选项2: 狂战士之怒 (berserker_rage)
#    汉明距离: 5, 置信度: 92.19%
# ❌ 选项3: 未识别 (unknown)
#    汉明距离: 999, 置信度: 0.00%
# ------------------------------------------------------------
#
# 识别成功率：2/3 = 66.7%
#
# 🎉 Phase 2 集成测试通过！
```

### 🎯 通过标准
- 识别成功率 >= 2/3（66%）
- 至少2个图标正确识别

### 📦 可交付物
- `tests/test_phase2_integration.py`

### 🔄 Git 提交
```bash
git add tests/test_phase2_integration.py
git commit -m "Add Phase 2 integration test with real game scenario"
git push origin master
```

### ❓ 如果识别率低怎么办？

**排查步骤：**
1. 打开 `output/phase2_icon_1_xxx.png` 等文件，检查裁剪是否准确
2. 如果裁剪不准确 → 回到 Step 1.3 重新标注 ROI
3. 如果裁剪准确但识别失败 → 检查图标库是否包含该强化
4. 如果图标库有但识别失败 → 图标质量问题，重新下载更清晰的图标

---

*Phase 3 决策层开发、Phase 4 整合测试的步骤会继续在文档中...*

---

# Phase 3: 决策层开发（Decision Layer）

> **目标**：实现 LLM 决策推荐
> **核心文件**：`src/decision.py`, `src/knowledge.py`

---

## Step 3.1 - 构建简化知识库

### 📝 测试标准
- `assets/knowledge_base.json` 文件存在
- 包含至少 10 个海克斯的描述
- 能正确加载和查询

### 🔧 实现步骤

**📝 创建知识库** `assets/knowledge_base.json`：
```json
{
  "cybernetic_shell": {
    "name_zh": "义体外壳",
    "category": "防御",
    "simple_desc": "受到伤害获得护盾",
    "good_for": ["战士", "坦克", "前排"],
    "bad_for": ["脆皮射手", "后排法师"],
    "priority": "A"
  },
  "berserker_rage": {
    "name_zh": "狂战士之怒",
    "category": "攻击",
    "simple_desc": "攻击速度大幅提升",
    "good_for": ["射手", "战士", "攻速流"],
    "bad_for": ["法师", "辅助"],
    "priority": "A"
  },
  "regeneration_aura": {
    "name_zh": "再生光环",
    "category": "防御",
    "simple_desc": "持续恢复生命值",
    "good_for": ["坦克", "消耗流", "持续作战"],
    "bad_for": ["爆发流", "快速团战"],
    "priority": "B"
  }
}
```

**🔍 创建测试** `tests/test_knowledge.py`：
```python
"""测试知识库"""
import json
import os
from src.config import ASSETS_DIR

def test_knowledge_base():
    """测试知识库加载"""
    kb_path = os.path.join(ASSETS_DIR, "knowledge_base.json")

    assert os.path.exists(kb_path), f"知识库文件不存在：{kb_path}"

    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)

    print(f"📚 知识库加载成功：{len(kb)} 个强化")

    for hex_id, data in kb.items():
        assert "name_zh" in data, f"{hex_id} 缺少 name_zh"
        assert "simple_desc" in data, f"{hex_id} 缺少 simple_desc"
        print(f"✅ {hex_id:25s} - {data['name_zh']}")

    print(f"\n🎉 知识库验证通过！")

if __name__ == "__main__":
    test_knowledge_base()
```

### ✅ 验证方法
```powershell
python tests/test_knowledge.py

# 预期输出：
# 📚 知识库加载成功：10 个强化
# ✅ cybernetic_shell       - 义体外壳
# ✅ berserker_rage         - 狂战士之怒
# ...
# 🎉 知识库验证通过！
```

### 🎯 通过标准
- 知识库包含至少 10 个条目
- 所有条目有必需字段

### 📦 可交付物
- `assets/knowledge_base.json`
- `tests/test_knowledge.py`

### 🔄 Git 提交
```bash
git add assets/knowledge_base.json tests/test_knowledge.py
git commit -m "Add simplified knowledge base"
git push origin master
```

---

## Step 3.2 - 配置 LLM API

### 📝 测试标准
- 创建 `.env` 文件存储 API Key
- 测试 API 调用成功

### 🔧 实现步骤

**📝 创建 `.env` 文件**（项目根目录）：
```env
# LLM API 配置
GEMINI_API_KEY=你的_Gemini_API_Key
CLAUDE_API_KEY=你的_Claude_API_Key

# 使用哪个 LLM（gemini, claude, deepseek）
LLM_PROVIDER=gemini
```

**📦 安装依赖**：
```powershell
pip install python-dotenv google-generativeai anthropic
pip freeze > requirements.txt
```

**🔍 创建测试** `tests/test_llm_api.py`：
```python
"""测试 LLM API 连接"""
import os
from dotenv import load_dotenv

def test_gemini_api():
    """测试 Gemini API"""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("⚠️ 未配置 GEMINI_API_KEY，跳过测试")
        return

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("说一句话：1+1=?")

    print(f"📡 Gemini API 测试")
    print(f"响应：{response.text[:100]}")

    assert response.text, "响应不应为空"
    print("✅ Gemini API 测试通过")

if __name__ == "__main__":
    test_gemini_api()
```

### ✅ 验证方法
```powershell
python tests/test_llm_api.py

# 预期输出：
# 📡 Gemini API 测试
# 响应：1+1等于2
# ✅ Gemini API 测试通过
```

### 🎯 通过标准
- API 调用成功，有响应

### 📦 可交付物
- `.env` 文件（**不提交到 Git**，已在 `.gitignore` 中）
- 更新的 `requirements.txt`
- `tests/test_llm_api.py`

### 🔄 Git 提交
```bash
git add requirements.txt tests/test_llm_api.py
git commit -m "Add LLM API configuration and test"
git push origin master
```

---

## Step 3.3 - 实现决策功能

### 📝 测试标准
- 给定英雄名和3个选项，LLM 返回推荐

### 🔧 实现步骤

**✅ 实现** `src/decision.py`：
```python
"""
决策模块
调用 LLM 给出海克斯选择建议
"""
import os
import json
from dotenv import load_dotenv
from src.config import ASSETS_DIR

load_dotenv()

def load_knowledge_base():
    """加载知识库"""
    kb_path = os.path.join(ASSETS_DIR, "knowledge_base.json")
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def call_llm_decision(hero_name, options):
    """
    调用 LLM 做决策

    Args:
        hero_name: 英雄名称
        options: list of dict，每个 dict 包含 hex_id, name_zh 等

    Returns:
        str: LLM 的推荐（包含选择+理由）
    """
    provider = os.getenv("LLM_PROVIDER", "gemini")

    # 构建 Prompt
    kb = load_knowledge_base()

    # 收集相关知识
    context_lines = []
    for opt in options:
        hex_id = opt['hex_id']
        if hex_id in kb:
            data = kb[hex_id]
            context_lines.append(f"- {data['name_zh']}：{data['simple_desc']}")

    context = "\n".join(context_lines)

    prompt = f"""你是祖安教练，说话直接粗暴。

当前英雄：{hero_name}
可选强化：
{context}

任务：选一个最适合的强化，给出一句话理由。
格式：选[强化名]！[理由，10字以内]

约束：
- 禁止用"建议"、"可以"等弱语气词
- 直接说"选XX"
- 理由要犀利简短
"""

    # 调用 API
    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        return response.text.strip()

    else:
        raise ValueError(f"不支持的 LLM provider: {provider}")

if __name__ == "__main__":
    # 快速测试
    test_options = [
        {"hex_id": "cybernetic_shell", "name_zh": "义体外壳"},
        {"hex_id": "berserker_rage", "name_zh": "狂战士之怒"},
    ]

    result = call_llm_decision("盖伦", test_options)
    print(f"决策结果：{result}")
```

**🔍 创建测试** `tests/test_decision.py`：
```python
"""测试决策功能"""
from src.decision import call_llm_decision

def test_decision():
    """测试 LLM 决策"""
    test_options = [
        {"hex_id": "cybernetic_shell", "name_zh": "义体外壳"},
        {"hex_id": "berserker_rage", "name_zh": "狂战士之怒"},
        {"hex_id": "regeneration_aura", "name_zh": "再生光环"},
    ]

    print("=" * 50)
    print("测试场景：英雄 = 盖伦（战士）")
    print("=" * 50)

    result = call_llm_decision("盖伦", test_options)

    print(f"\n📢 LLM 推荐：")
    print(result)

    # 简单验证
    assert len(result) > 0, "结果不应为空"
    assert "选" in result, "结果应包含"选"字"

    print("\n✅ 决策测试通过")

if __name__ == "__main__":
    test_decision()
```

### ✅ 验证方法
```powershell
python tests/test_decision.py

# 预期输出示例：
# ==================================================
# 测试场景：英雄 = 盖伦（战士）
# ==================================================
#
# 📢 LLM 推荐：
# 选义体外壳！战士需要硬度保命
#
# ✅ 决策测试通过
```

### 🎯 通过标准
- LLM 返回推荐
- 格式包含"选XX"

### 📦 可交付物
- `src/decision.py`
- `tests/test_decision.py`

### 🔄 Git 提交
```bash
git add src/decision.py tests/test_decision.py
git commit -m "Implement LLM decision logic"
git push origin master
```

---

# Phase 4: 整合与测试（Integration & Testing）

> **目标**：串联所有模块，实现完整流程

---

## Step 4.1 - 实现主流程

### 📝 测试标准
- 按 F9 触发完整流程：截图 → 识别 → 决策 → 输出

### 🔧 实现步骤

**✅ 实现** `src/main.py`：
```python
"""
主程序
完整的 MVP 流程
"""
import os
import keyboard
from datetime import datetime
from src.capture import capture_screen
from src.config import OUTPUT_DIR, ROI_CONFIG, DEBUG_MODE
from src.recognition import match_three_icons
from src.decision import call_llm_decision

def process_hex_choice():
    """处理海克斯选择的完整流程"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n" + "=" * 60)
    print(f"⏰ 触发时间：{datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

    # Step 1: 截图
    print("\n📸 Step 1/4: 截图中...")
    screenshot = capture_screen()

    if DEBUG_MODE:
        debug_path = os.path.join(OUTPUT_DIR, f"main_{timestamp}.png")
        screenshot.save(debug_path)
        print(f"   已保存：{debug_path}")

    # Step 2: ROI 裁剪
    print("\n✂️ Step 2/4: 裁剪图标...")
    icons = []
    for i in [1, 2, 3]:
        roi = ROI_CONFIG[f"hex_choice_{i}"]
        if roi:
            icon = screenshot.crop(roi)
            icons.append(icon)
            print(f"   图标{i} 裁剪完成")

    # Step 3: 识别
    print("\n🔍 Step 3/4: 识别图标...")
    results = match_three_icons(icons[0], icons[1], icons[2])

    for r in results:
        status = "✅" if r['hex_id'] != "unknown" else "❌"
        print(f"   {status} 选项{r['position']}: {r['name_zh']} (置信度: {r['confidence']:.1%})")

    # 过滤掉未识别的
    valid_results = [r for r in results if r['hex_id'] != "unknown"]

    if len(valid_results) == 0:
        print("\n❌ 没有识别出任何图标，可能原因：")
        print("   - ROI 坐标不准确")
        print("   - 图标库不完整")
        return

    # Step 4: LLM 决策
    print("\n🤖 Step 4/4: AI 决策中...")

    # 简化：假设英雄名固定（MVP阶段不识别英雄）
    hero_name = "未知英雄"  # TODO: 后续版本识别英雄名

    decision = call_llm_decision(hero_name, valid_results)

    print("\n" + "=" * 60)
    print("📢 推荐结果：")
    print("=" * 60)
    print(decision)
    print("=" * 60)

    # TODO: Step 5 语音播报（Phase 4 后续步骤）

def start_mvp_service():
    """启动 MVP 服务"""
    print("\n" + "🎮" * 30)
    print("Hex-Strategist MVP 服务已启动")
    print("🎮" * 30)
    print("\n操作说明：")
    print("  F9  - 触发决策（在海克斯选择界面按）")
    print("  ESC - 退出服务")
    print("\n等待按键...")

    keyboard.add_hotkey('f9', process_hex_choice)
    keyboard.wait('esc')

    print("\n服务已停止")

if __name__ == "__main__":
    start_mvp_service()
```

### ✅ 验证方法（游戏内测试）

```powershell
# 1. 启动服务
python src/main.py

# 2. 进入游戏，触发海克斯选择界面

# 3. 按 F9

# 预期输出：
# ===========================================================
# ⏰ 触发时间：16:30:45
# ===========================================================
#
# 📸 Step 1/4: 截图中...
#    已保存：output/main_20250127_163045.png
#
# ✂️ Step 2/4: 裁剪图标...
#    图标1 裁剪完成
#    图标2 裁剪完成
#    图标3 裁剪完成
#
# 🔍 Step 3/4: 识别图标...
#    ✅ 选项1: 义体外壳 (置信度: 95.3%)
#    ✅ 选项2: 狂战士之怒 (置信度: 92.2%)
#    ❌ 选项3: 未识别 (置信度: 0.0%)
#
# 🤖 Step 4/4: AI 决策中...
#
# ===========================================================
# 📢 推荐结果：
# ===========================================================
# 选义体外壳！需要保命
# ===========================================================
```

### 🎯 通过标准
- 完整流程跑通
- 至少识别出 1 个图标
- LLM 给出推荐

### 📦 可交付物
- `src/main.py`

### 🔄 Git 提交
```bash
git add src/main.py
git commit -m "Implement main MVP pipeline"
git push origin master
```

---

## Step 4.2 - 添加语音播报

### 📝 测试标准
- 决策结果能通过语音播报

### 🔧 实现步骤

**📦 安装依赖**：
```powershell
pip install edge-tts pygame
pip freeze > requirements.txt
```

**✅ 实现** `src/tts.py`：
```python
"""
语音播报模块
使用 Edge-TTS
"""
import os
import asyncio
import edge_tts
import pygame
from src.config import OUTPUT_DIR

async def text_to_speech_async(text, output_path):
    """异步文本转语音"""
    # 使用中文女声
    voice = "zh-CN-XiaoxiaoNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def speak(text):
    """
    播报文本

    Args:
        text: 要播报的文字
    """
    # 生成音频文件
    audio_path = os.path.join(OUTPUT_DIR, "tts_temp.mp3")

    # 同步调用异步函数
    asyncio.run(text_to_speech_async(text, audio_path))

    # 播放音频
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # 等待播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 清理
    pygame.mixer.quit()

if __name__ == "__main__":
    # 测试
    print("测试语音播报...")
    speak("选义体外壳！需要保命")
    print("✅ 播报完成")
```

**🔍 测试**：
```powershell
python src/tts.py
# 应该听到语音：选义体外壳！需要保命
```

**📝 集成到主流程**（在 `src/main.py` 中）：
```python
# 在 src/main.py 顶部添加：
from src.tts import speak

# 在 process_hex_choice() 函数末尾添加：
    # Step 5: 语音播报
    print("\n🔊 Step 5/5: 语音播报...")
    speak(decision)
    print("✅ 播报完成")
```

### ✅ 验证方法
```powershell
python src/main.py
# 按 F9，应该听到语音播报
```

### 🎯 通过标准
- 能听到完整的推荐语音

### 📦 可交付物
- `src/tts.py`
- 更新的 `src/main.py`
- 更新的 `requirements.txt`

### 🔄 Git 提交
```bash
git add src/tts.py src/main.py requirements.txt
git commit -m "Add TTS voice feedback"
git push origin master
```

---

## Step 4.3 - 最终测试与文档

### 📝 测试标准
- 在游戏中测试至少 5 次
- 识别率 >= 60%
- 决策合理

### 🔧 实现步骤

**📊 创建测试记录表** `tests/final_test_log.md`：
```markdown
# MVP 最终测试记录

## 测试环境
- 日期：2025-01-27
- 游戏模式：海克斯大乱斗
- 分辨率：1920x1080

## 测试结果

| 次数 | 识别1 | 识别2 | 识别3 | 识别率 | LLM推荐 | 是否合理 |
|-----|-------|-------|-------|--------|---------|---------|
| 1   | ✅ 义体 | ✅ 狂战 | ❌     | 66%    | 选义体   | ✅ 是    |
| 2   |       |       |       |        |         |         |
| 3   |       |       |       |        |         |         |
| 4   |       |       |       |        |         |         |
| 5   |       |       |       |        |         |         |

## 统计
- 平均识别率：XX%
- LLM 决策合理率：XX%

## 问题记录
1. XXX
2. XXX
```

**📝 更新 README.md**：
```markdown
# Hex-Strategist MVP

英雄联盟海克斯大乱斗决策系统 - MVP版本

## 功能
✅ 截图识别海克斯图标
✅ AI 决策推荐
✅ 语音播报结果

## 使用方法

### 1. 安装依赖
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 配置 API Key
创建 `.env` 文件：
\`\`\`env
GEMINI_API_KEY=你的Key
LLM_PROVIDER=gemini
\`\`\`

### 3. 配置 ROI（首次使用）
- 进游戏截图海克斯界面
- 标注3个图标坐标
- 填入 `src/config.py`

### 4. 启动服务
\`\`\`bash
python src/main.py
\`\`\`

### 5. 游戏内使用
- 触发海克斯选择界面
- 按 F9 键
- 等待语音播报

## 目录结构
\`\`\`
Hex_Strategist/
├── src/              # 源代码
│   ├── capture.py    # 截图模块
│   ├── recognition.py # 识别模块
│   ├── decision.py   # 决策模块
│   ├── tts.py        # 语音模块
│   └── main.py       # 主程序
├── tests/            # 测试脚本
├── assets/           # 资源文件
│   ├── hex_icons/    # 图标库
│   └── knowledge_base.json # 知识库
└── output/           # 输出目录
\`\`\`

## 测试
详见 [Development_Log.md](Development_Log.md)

## 已知限制（MVP版本）
- 仅支持 1920x1080 分辨率
- 图标库有限（约10个）
- 不识别英雄名（默认通用推荐）
- 不考虑已有强化（首次使用）

## 下一步计划
详见白皮书 Phase 2 规划
```

### ✅ 验证方法
- 实际游戏中测试 5 次
- 填写测试记录表
- 评估是否达到 MVP 目标

### 🎯 通过标准
- 平均识别率 >= 60%
- LLM 决策合理率 >= 80%
- 完整流程能跑通

### 📦 可交付物
- `tests/final_test_log.md`
- 更新的 `README.md`

### 🔄 Git 提交
```bash
git add tests/final_test_log.md README.md
git commit -m "Complete MVP: Add final test log and documentation"
git push origin master
```

---

# 🎉 MVP 完成检查清单

完成以下所有项，MVP 即可交付：

## Phase 0: 环境准备
- [ ] Step 0.1 - Python 安装
- [ ] Step 0.2 - Git 配置
- [ ] Step 0.3 - 服务器仓库
- [ ] Step 0.4 - 项目结构
- [ ] Step 0.5 - 虚拟环境
- [ ] Step 0.6 - 依赖库安装
- [ ] Step 0.7 - VSCode 配置（可选）
- [ ] Step 0.8 - 配置文件

## Phase 1: 感知层
- [ ] Step 1.1 - 基础截图
- [ ] Step 1.2 - 热键触发
- [ ] Step 1.3 - ROI 标注
- [ ] Step 1.4 - OCR 识别
- [ ] Step 1.5 - 集成测试

## Phase 2: 识别层
- [ ] Step 2.1 - 图标素材
- [ ] Step 2.2 - pHash 计算
- [ ] Step 2.3 - 图标匹配
- [ ] Step 2.4 - 游戏内测试

## Phase 3: 决策层
- [ ] Step 3.1 - 知识库
- [ ] Step 3.2 - API 配置
- [ ] Step 3.3 - 决策逻辑

## Phase 4: 整合
- [ ] Step 4.1 - 主流程
- [ ] Step 4.2 - 语音播报
- [ ] Step 4.3 - 最终测试

## 文档
- [ ] README.md 完整
- [ ] 测试记录完成
- [ ] 开发日志更新

---

**下一步**：录制演示视频，准备面试讲解材料

---

# 附录：常用 Git 命令速查

```bash
# 查看状态
git status

# 添加所有更改
git add .

# 提交
git commit -m "描述信息"

# 推送到服务器
git push origin master

# 查看提交历史
git log --oneline

# 查看最近的更改
git diff
```

---

**文档版本**：v1.0
**创建日期**：2025-12-27
**预计完成**：2026-02-27（60天）
**作者**：Ezreau
