# Project Hex-Strategist: 深度演训白皮书
## 基于多模态 RAG、实时视觉感知与人格化 Agent 的英雄联盟"海克斯大乱斗（ARAM）"决策系统

---

## 第 0 章：项目战略愿景 (Strategic Mission & Purpose)

### 0.1 核心定位
针对《英雄联盟》海克斯大乱斗（Roguelike模式）的高随机性与强协同性，构建一个"懂局势、会构筑、有灵魂"的实时决策 Agent。

### 0.2 交付目标
- **技术突破**：实现极低延迟（<1.5s）的"视觉-大脑-交互"全链路闭环
- **工程价值**：展示非科班开发者通过 AI 驱动完成复杂分布式系统设计与落地的实战能力
- **职业目标**：作为从制造业转行至 AI Agent 开发岗位的核心作品集项目

### 0.3 核心场景
1. **海克斯强化三选一**：基于当前英雄与已有增益的协同效应（Synergy）给出秒级建议
2. **动态构筑修正**：随随机强化的改变，实时重构出装路线（如 AP 转肉、攻速转特效）
3. **战术预警**：识别敌方关键海克斯威胁，通过语音/手机推送发出战术提醒

---

## 第 0.5 章：开发者画像与资源约束 (Developer Profile & Constraints)

### 0.5.1 技术背景
- **编程经验**：Python 阅读经验，无实战项目经验
- **AI 经验**：
  - 使用过 PaddleOCR
  - 无向量数据库、LLM API 开发经验
  - 仅在 LobeHub 等应用中调用过大模型
- **定位**：AI Agent 开发新手 + 编程新手

### 0.5.2 硬件与基础设施

#### 本地服务器 (Ubuntu Server 22.04 LTS)
- **CPU**：Intel i3-10100F (4核8线程)
- **内存**：16GB RAM + 16GB Swap
- **GPU**：GTX 1650 Super
- **存储**：
  - 240GB SSD (系统盘)
  - 500GB HDD (挂载于 /hdd500)
  - 4TB HDD (挂载于 /hdd4000)
- **网络**：固定内网 IP 192.168.1.200
- **用途**：Git 仓库、测试环境、未来部署平台

#### 云服务器 (VPS - 洛杉矶)
- **IP**：74.48.63.24
- **域名**：ai.superu.top (Cloudflare 托管)
- **现有服务**：Docker Compose 部署的 LobeHub
- **用途**：后期分布式架构的云端决策节点

#### Windows 游戏机
- **用途**：运行《英雄联盟》+ 主开发环境
- **状态**：待确认 Python 环境

### 0.5.3 API 资源
- **Google AI Studio**：Gemini API Key (已有)
- **中转 API**：支持 Claude、GPT-4、DeepSeek、GLM-4
- **额度**：无需考虑限制

---

## 第 0.6 章：双阶段架构策略 (Two-Phase Architecture)

### 设计哲学：先跑通，再优化

```
Phase 1: MVP 单机版          Phase 2: 分布式完整版
   (简化版)          →          (完整版)
```

### Phase 1: MVP 简化架构

#### 核心原则
- **单机运行**：全部逻辑在 Windows 游戏机上运行
- **最小依赖**：避免复杂的服务编排
- **快速验证**：专注核心功能（海克斯三选一）

#### 技术栈对比

| 模块 | 完整版设计 | MVP 简化方案 |
|-----|-----------|-------------|
| **架构** | 微服务分布式 | 单机 Python 脚本 |
| **知识库** | ChromaDB 向量检索 | JSON 文件 + Prompt 工程 |
| **部署** | 本地服务器 + 云端协同 | Windows 本地运行 |
| **交互** | 语音 + 手机推送 | 仅语音 (Edge-TTS) |
| **状态管理** | Redis + FSM | 内存变量 |

#### MVP 数据流

```
┌────────────────────────────────────────────────┐
│          Windows 游戏机 (单机脚本)               │
│                                                │
│  [游戏画面]                                     │
│      ↓                                         │
│  [截屏模块] mss库                               │
│      ↓                                         │
│  [ROI裁剪] 仅处理屏幕5%关键区域                  │
│      ↓                                         │
│  [图像识别]                                     │
│      ├─→ pHash指纹匹配 (海克斯图标)             │
│      └─→ PaddleOCR (KDA/金币等)                │
│      ↓                                         │
│  [组装上下文]                                   │
│      ├─→ 当前英雄                               │
│      ├─→ 识别出的三个海克斯选项                  │
│      └─→ 从JSON加载相关知识                     │
│      ↓                                         │
│  [调用LLM API]                                 │
│      └─→ Gemini/Claude/DeepSeek              │
│      ↓                                         │
│  [语音播报] Edge-TTS                           │
│      └─→ 通过耳机输出指令                       │
└────────────────────────────────────────────────┘
```

### Phase 2: 分布式完整架构

#### 系统拓扑

```
┌──────────────────────┐
│   Windows 游戏机      │
│  ┌────────────────┐  │
│  │ Perception     │  │
│  │ Service        │  │
│  │ - mss截屏      │  │
│  │ - pHash识别    │  │
│  │ - PaddleOCR    │  │
│  └────────┬───────┘  │
└───────────┼──────────┘
            │ HTTP/gRPC
            ↓
┌──────────────────────┐
│  Ubuntu 本地服务器    │
│  ┌────────────────┐  │
│  │ Knowledge      │  │
│  │ Service        │  │
│  │ - ChromaDB     │  │
│  │ - 向量检索     │  │
│  └────────┬───────┘  │
│           │          │
│  ┌────────▼───────┐  │
│  │ Decision       │  │
│  │ Agent          │  │
│  │ - CoT推理链    │  │
│  │ - 人格化引擎   │  │
│  └────────┬───────┘  │
└───────────┼──────────┘
            │
            ↓
┌──────────────────────┐
│  多端交互分发         │
│  ┌────────────────┐  │
│  │ Interaction    │  │
│  │ Service        │  │
│  │ - Edge-TTS     │  │
│  │ - Bark推送     │  │
│  │ - Redis状态    │  │
│  └────────────────┘  │
└──────────────────────┘
```

#### 演进路径

| 升级项 | 改造内容 |
|-------|---------|
| **感知层** | 封装成 FastAPI 服务，Windows 端定时上报 |
| **知识层** | JSON → ChromaDB，增加语义相似度检索 |
| **决策层** | 本地调用 → 部署到服务器，加入 Chain-of-Thought |
| **交互层** | 单一TTS → 流式语音 + Webhook 手机推送 |
| **状态管理** | 内存变量 → Redis FSM |

---

## 第 0.8 章：游戏机制修正（基于实际验证）

### 0.8.1 海克斯大乱斗核心机制（2025年实测）

#### Reroll（重掷）机制
- **成本**：❌ **不需要金币**（与Arena模式不同）
- **次数**：每次强化选择界面**重置为1次**（用不完就浪费）
- **范围**：**Per-slot 刷新**（可单独刷新某个槽位，不是刷新全部3个）
- **策略影响**：决策可以更激进，不需要"节省reroll"的考虑

#### 强化选择时机与时间约束
- **触发条件**：Level 3/7/11/15 或死亡时
- **选择时限**：30秒倒计时
- **系统响应时间预算**：
  ```
  截图(50ms) + 识别(300ms) + LLM(1000ms) + 语音(2500ms) ≈ 4秒
  ```
- **关键约束**：必须在**25秒内**完成决策播报，留5秒给用户操作

#### 模式对比澄清（重要）

| 特性 | Arena (2v2v2v2) | ARAM: Mayhem | 本项目目标 |
|------|----------------|--------------|-----------|
| Reroll机制 | 全局共享，可累积 | 每次重置，独立 | ✅ ARAM: Mayhem |
| Reroll成本 | 无金币成本 | 无金币成本 | ✅ 已验证 |
| 选择时机 | 特定回合 | Level 3/7/11/15 | ✅ ARAM: Mayhem |
| 刷新范围 | Per-slot | Per-slot | ✅ 已验证 |
| Overwolf API支持 | ✅ 有augments API | ⚠️ 未知（新模式） | 待验证 |

> **⚠️ 关键教训**：白皮书初版基于Arena模式设计，实际游戏为ARAM: Mayhem，机制有差异但核心相同。

---

## 第 0.9 章：MVP技术边界与"不做什么"

### 0.9.1 MVP核心原则
**"先证明可行，再打磨体验"**

### 0.9.2 明确的技术边界

#### ✅ MVP 必做功能（Week 1-4）

| 模块 | 功能 | 技术方案 | 验证标准 |
|------|------|---------|---------|
| **感知层** | 截图识别当前3个强化选项 | mss + pHash（大图标80x80） | 识别率 > 80% |
| **决策层** | 推荐最优选项 | LLM API（Gemini/Claude二选一） | 能给出合理建议 |
| **交互层** | 按键触发（F9） | keyboard库监听 | 按键响应 < 0.5s |
| **输出层** | 语音播报结果 | Edge-TTS | 延迟 < 2s |

#### ❌ MVP 不做功能（延后到 V2/V3）

| 功能 | 为什么不做 | 何时做 |
|------|-----------|--------|
| ❌ Reroll判断 | 增加决策复杂度，用户可自行判断 | V2：加入"选X" vs "刷Y"判断 |
| ❌ 自动检测界面 | 需要复杂的变化监听，MVP用按键触发即可 | V2：实现智能检测 |
| ❌ TAB识别已有强化 | 小图标识别率未知，用简单记录代替 | V2：如pHash测试通过 |
| ❌ 装备识别 | 非核心功能，MVP只关注强化选择 | V2：装备-海克斯联动 |
| ❌ Overwolf插件 | 开发复杂度高，API不确定 | V3：如MVP成功 |
| ❌ 分布式架构 | 过度设计，MVP本地单机即可 | V3：性能瓶颈时考虑 |
| ❌ 知识库向量化 | RAG系统复杂，MVP用JSON即可 | V3：知识库 > 100条时 |
| ❌ 多模型对比 | 浪费时间，选一个能用的就行 | 不做：没有必要 |

### 0.9.3 简化的MVP决策流程

```python
# MVP 决策逻辑（极简版）
def mvp_decision(hero, current_options):
    """
    输入：英雄名 + 当前3个选项
    输出：推荐哪个 + 一句话理由

    不考虑：
    - ❌ 已有强化（用简单记录代替）
    - ❌ Reroll建议（用户自己决定）
    - ❌ 装备协同（V2功能）
    """
    prompt = f"""
    你是祖安教练，说话直接。

    英雄: {hero}
    选项: {current_options}

    任务: 选一个，一句话理由（禁止"建议"等弱语气词）
    输出格式: 选[选项名]！[理由]
    """
    return llm_call(prompt)
```

### 0.9.4 技术债务清单（待V2偿还）

| 债务项 | 影响 | 偿还优先级 |
|--------|------|----------|
| 1. 已有强化识别 | 决策无法考虑协同效应 | P1（高） |
| 2. Reroll建议 | 浪费每次的免费刷新机会 | P2（中） |
| 3. 装备识别 | 无法给出装备-海克斯联动建议 | P3（低） |
| 4. 自动检测 | 用户每次要手动按F9 | P2（中） |

> **核心理念**：MVP的目标是"证明核心技术可行"，不是"做出完美产品"。过度设计会拖延进度，导致项目失败。

---

## 第 1 章：MVP 开发计划（分阶段实施）

### Week 1: 感知层 - "让程序看到游戏"（简化版）
**目标**：能截图、能保存、能跑起来

#### 任务清单
- [ ] **环境搭建**
  - 安装 Python 3.10+
  - 安装依赖：`pip install mss Pillow paddleocr keyboard`
  - 测试导入：`import mss` 能跑就行

- [ ] **截屏测试**
  - 写一个 `test_capture.py`：按F9截图并保存
  - 截取游戏全屏，保存为 `screenshot_001.png`
  - **验证标准**：能截图就行，不管性能

- [ ] **ROI 标注**
  - 进游戏，截取海克斯选择界面
  - 用画图工具标注3个强化图标的位置
  - 记录坐标到 `roi_config.py`
  - ❌ **删除**：不做不同分辨率适配（MVP只支持1920x1080）

- [ ] **基础 OCR 测试**
  - 用PaddleOCR识别英雄名字（截图上任何文字都行）
  - 打印结果：`print(ocr_result)`
  - ❌ **删除**：KDA/金币识别（MVP阶段用不上）
  - ❌ **删除**：建立测试截图库（过早优化）

**交付物**：
- `test_capture.py` - 能按F9截图
- `roi_config.py` - 记录的坐标
- 1-2张测试截图

---

### Week 2: 识别层 - "pHash 能识别吗"（简化版）
**目标**：证明 pHash 识别可行，能匹配就行

#### 任务清单
- [ ] **收集 10-20 个常见强化图标**
  - 从 Wiki/Google 下载（不是200+）
  - 保存到 `assets/hex_icons/` 文件夹
  - 命名规范：`augment_name.png`（如 `cybernetic_shell.png`）
  - ❌ **删除**：手动分类（过早优化）

- [ ] **pHash 基础测试**
  - 安装 `imagehash`：`pip install imagehash`
  - 写一个 `test_phash.py`：计算一个图标的哈希值
  - 测试：同一图标的不同截图能否匹配
  - **验证标准**：汉明距离 < 10 就算成功

- [ ] **简单匹配函数**
  - 实现 `match_augment(screenshot_crop)` 函数
  - 遍历图标库，返回最相似的那个
  - 打印结果：`匹配到: 义体外壳, 距离: 5`
  - ❌ **删除**：边缘情况处理（V2再说）

- [ ] **【新增】装备图标识别测试**
  - 收集 5-10 个常见装备图标
  - 测试 pHash 能否识别装备
  - **目的**：为 V2 的装备-海克斯联动做准备
  - 不集成到主流程，只做可行性验证

- [ ] ❌ **删除：性能优化**（MVP不需要）

**交付物**：
- `test_phash.py` - pHash测试脚本
- `assets/hex_icons/` - 10-20个图标
- `assets/item_icons/` - 5-10个装备图标（可选）
- 识别成功的截图证据

---

### Week 3: 决策层 - "AI 能给建议吗"（极简版）
**目标**：LLM 能返回结果，不求最优

#### 任务清单
- [ ] **简化知识库**
  - 手动整理 **10个** 常见海克斯的描述（不是50个）
  - 每个海克斯只写：名字 + 一句话简介
  - 存储为 `knowledge_base.json`
  - ❌ **删除**：协同标注、优先级评分（V2再做）

- [ ] **极简 Prompt**
  - 选一个 LLM API（Gemini 或 Claude，二选一）
  - 写一个最简单的 Prompt：
    ```
    英雄：{hero}
    选项：{options}
    任务：选一个，一句话理由
    ```
  - ❌ **删除**：不考虑已有强化、不考虑reroll
  - ❌ **删除**：多模型对比（浪费时间）

- [ ] **API 调用测试**
  - 封装 `call_llm(prompt)` 函数
  - 测试能否返回结果
  - 打印：`选义体！你是战士需要坦度`
  - ❌ **删除**：错误重试机制（V2再加）
  - ❌ **删除**：调用日志（过度设计）

- [ ] **【新增】AugmentTracker 记录类**
  - 实现简单的 Session 记录
  - ```python
    class AugmentTracker:
        def __init__(self):
            self.augments = []
        def add(self, name):
            self.augments.append(name)
    ```
  - 替代 TAB 识别方案

**交付物**：
- `knowledge_base.json` - 10个海克斯描述
- `decision.py` - LLM调用函数
- `augment_tracker.py` - 简单记录类

---

### Week 4: 整合 - "能跑就行"（简化版）
**目标**：串起来，能演示，不崩溃

#### 任务清单
- [ ] **主流程串联**
  - 写一个 `main.py`：按F9触发完整流程
  - 流程：截图 → 识别 → 调用LLM → 语音播报
  - ❌ **删除**：状态机设计（过度设计）
  - ❌ **删除**：自动检测界面（V2功能）

- [ ] **语音播报**
  - 集成 Edge-TTS：`pip install edge-tts`
  - 测试语音：`edge-tts --text "选义体" --write-media output.mp3`
  - 播放音频：用 `pygame` 或直接调用系统播放器
  - ❌ **删除**：延迟优化（能播就行）

- [ ] **实战测试**
  - 进游戏测试几局
  - 记录：识别率、延迟、崩溃
  - 修复**最严重的bug**
  - ❌ **删除**：全面调试（够用就行）

- [ ] **最简文档**
  - 写一个 `README.md`：安装步骤 + 使用方法
  - 录一个演示视频
  - ❌ **删除**：面试讲解脚本（临场发挥）

**交付物**：
- `main.py` - 能跑的主程序
- `README.md` - 简单文档
- `demo.mp4` - 演示视频

---

## 第 1.5 章：识别已有强化的技术方案（V2规划）

### 1.5.1 技术挑战
- 首次使用时，系统不知道用户之前选了什么
- 决策无法考虑协同效应

### 1.5.2 MVP方案：简单记录（已在Week 3实现）

```python
# augment_tracker.py
class AugmentTracker:
    """Session级别的强化记录"""
    def __init__(self):
        self.augments = []  # 本局游戏的强化列表

    def add(self, augment_name):
        """用户选择后记录"""
        self.augments.append(augment_name)

    def get_existing(self):
        """返回已有强化"""
        return self.augments

    def clear(self):
        """新游戏清空"""
        self.augments = []
```

**优点**：
- ✅ 零识别成本，100%准确
- ✅ 开发简单快速
- ✅ 适合MVP快速验证

**缺点**：
- ❌ 首次使用无历史记录
- ❌ 依赖用户采纳系统建议

### 1.5.3 V2方案：TAB面板识别（备选）

#### 技术路径
1. 用户按TAB → 打开记分板
2. 系统截图 → 定位强化图标区域（ROI）
3. pHash识别小图标（25-30像素）

#### ROI坐标标注（基于实际截图）

```python
# TAB面板强化图标区域（1920x1080分辨率）
TAB_AUGMENT_ROIS = {
    "right_team": {  # 蓝色方显示区域
        "player_1": (990, 130, 1150, 170),
        "player_2": (990, 200, 1150, 240),
        "player_3": (990, 270, 1150, 310),
        "player_4": (990, 340, 1150, 380),
        "player_5": (990, 410, 1150, 450),
    }
}
```

#### 实施前提（需Week 2验证）
- [ ] pHash对30x30小图标的识别率 > 80%
- [ ] 能准确定位己方英雄的位置（第几个玩家）

#### 用户交互流程

```python
def get_existing_augments():
    """获取已有强化（混合方案）"""

    # 1. 优先从记录读取
    existing = tracker.get_existing()
    if existing:
        return existing

    # 2. 记录为空，提示用户
    speak("按TAB让我看看你的强化，或按空格跳过")
    key = wait_for_key(['tab', 'space'], timeout=5)

    if key == 'tab':
        time.sleep(0.5)  # 等待面板动画
        screenshot = capture()
        existing = recognize_from_tab(screenshot)
        speak("看到了")
        return existing
    else:
        return []  # 跳过，不考虑历史
```

### 1.5.4 V2实施条件
- Week 2的小图标识别测试通过
- MVP完成后有时间做优化
- 用户反馈"需要考虑协同效应"

---

## 第 1.6 章：技术风险评估与应对

### 1.6.1 反外挂风险

#### mss截图的安全性分析

| 检测类型 | 风险等级 | 原因 | 应对策略 |
|---------|---------|------|---------|
| 进程注入 | ✅ 无风险 | mss不注入游戏进程 | - |
| 内存读写 | ✅ 无风险 | 不读取游戏内存 | - |
| API Hook | ✅ 无风险 | 不Hook DirectX/OpenGL | - |
| 自动化操作 | ⚠️ 中风险 | MVP无自动操作 | 只做信息提示，不做自动点击 |
| 第三方程序检测 | ⚠️ 中风险 | Vanguard可能检测Python进程 | 测试环境使用，加免责声明 |

**结论**：
- MVP阶段（截图+语音提示）：**风险很低**
- ❌ **绝对不做**：自动点击、自动选择
- ✅ **在README加免责声明**

#### 免责声明模板

```markdown
## ⚠️ 免责声明

本项目仅用于技术学习和展示，不鼓励在实际游戏中使用。

使用本工具可能违反《英雄联盟》服务条款，账号封禁风险自负。

建议：
- 仅在测试环境使用
- 不要在排位赛使用
- 不要开启自动化功能（如有）
```

### 1.6.2 Overwolf 方案不可行性分析

#### API局限性调研结果

```
✅ Overwolf可以获取：
- 英雄信息、KDA、装备
- 游戏模式（ARAM/召唤师峡谷/Arena）
- 已选择的augments（如果API支持）

❌ Overwolf大概率无法获取：
- 当前界面显示的"待选的3个augments"
- 原因：临时UI状态通常不暴露给外部API
```

#### 决策记录

- **MVP阶段**：放弃Overwolf，使用纯Python方案（截图识别）
- **V2验证**：如果Overwolf能获取已选augments，可做混合方案（API获取基础信息 + 截图识别选项）
- **V3考虑**：如果MVP成功且有用户需求，再做Overwolf插件版本

### 1.6.3 pHash识别率风险

#### 不确定因素
1. 小图标（25-30px）识别率未知
2. 游戏光效、动画可能影响识别
3. 不同分辨率下图标缩放

#### 应对策略：分级Fallback

```python
def recognize_with_fallback(screenshot):
    """多重保障识别"""

    # 1. 尝试pHash（快，准确率高）
    result = recognize_with_phash(screenshot)
    if result['confidence'] > 0.8:
        return result

    # 2. 降级到OCR（慢但更宽容）
    result_ocr = recognize_with_ocr(screenshot)
    if result_ocr:
        return result_ocr

    # 3. 最终兜底：让用户确认
    speak("识别不清，是哪三个？说数字")
    user_input = get_voice_input()  # V3功能
    return parse_user_input(user_input)
```

#### 测试标准（Week 2验证）
- 大图标（80x80）识别率 > **90%** → MVP可行
- 小图标（30x30）识别率 > **80%** → V2可做TAB识别
- 小图标识别率 < 80% → 放弃TAB方案，只用Session记录

---

## 第 2 章：完整版系统架构设计 (Full-Scale Architecture)

> ⚠️ **注意**：本章内容为 V2/V3 规划，MVP阶段**不实施**。

### 2.1 设计哲学
**感知本地化、大脑云端化、反馈多模态**

### 2.2 模块架构 (Microservices Logic)

#### 2.2.1 Perception Service (本地 - Windows)
- **职责**：高频截屏 + 图像指纹匹配 + OCR
- **技术栈**：Python + mss + PaddleOCR + pHash
- **性能要求**：
  - 截屏频率：2次/秒
  - ROI 处理延迟：< 50ms
  - 识别准确率：> 95%

#### 2.2.2 Knowledge Service (服务器 - Ubuntu)
- **职责**：向量检索 + 知识图谱查询
- **技术栈**：ChromaDB + FastAPI
- **数据源**：
  - Riot DataDragon (官方 API)
  - 英雄联盟 Wiki
  - 大乱斗平衡数据 (Aura)
- **检索优化**：
  - 基于 "当前英雄名" 的强制标签过滤
  - 响应时间：< 100ms

#### 2.2.3 Decision Agent (云端 - VPS)
- **职责**：CoT 推理 + 人格化输出
- **技术栈**：DeepSeek V3 API / Claude Sonnet
- **推理链**：
  1. **Identify**：识别局势压力位
  2. **Synergize**：计算协同分数
  3. **Execute**：输出战术指令

#### 2.2.4 Interaction Service (分发)
- **职责**：多模态反馈分发
- **技术栈**：Edge-TTS + Bark/PushDeer Webhook
- **状态管理**：Redis FSM

---

## 第 3 章：感知层详细设计 (Perception Layer)

### 3.1 特种识别引擎 (Hybrid Recognition)

#### 3.1.1 图标识别 (Visual Hashing)
- **算法选择**：pHash（感知哈希）
- **指纹库规模**：200+ 海克斯图标
- **匹配策略**：
  - 汉明距离阈值：< 10
  - 多候选排序：按相似度降序
- **性能指标**：单次匹配 < 10ms

#### 3.1.2 文本补全 (OCR)
- **工具**：PaddleOCR
- **识别目标**：
  - 英雄名称
  - KDA（击杀/死亡/助攻）
  - 金币数量
  - 海克斯刷新次数
- **后处理**：正则表达式清洗 + 字典校正

### 3.2 性能优化 (Performance)

#### 3.2.1 ROI 裁剪策略
```python
# 1920x1080 分辨率下的关键区域
ROI_CONFIG = {
    "hex_choice": (750, 300, 1170, 700),  # 三选一区域
    "hero_name": (50, 50, 300, 100),       # 英雄名
    "kda": (1600, 50, 1870, 100),          # KDA显示
}
```
- 裁剪后仅处理屏幕 5% 区域
- 确保不影响游戏帧率（< 1% GPU 占用）

#### 3.2.2 缓存机制
- 图标指纹预加载到内存
- OCR 结果缓存（避免重复识别相同画面）

---

## 第 4 章：知识层详细设计 (Knowledge Layer)

### 4.1 MVP 知识库设计

#### 4.1.1 JSON 结构
```json
{
  "hex_id": "cybernetic_shell",
  "name": "义体外壳",
  "category": "防御",
  "description": "受到伤害时获得护盾",
  "synergy": {
    "heroes": ["蒙多医生", "石头人", "奥恩"],
    "hexes": ["再生光环", "霸体"],
    "priority": "A"
  },
  "avoid_with": ["脆皮射手", "刺客"]
}
```

#### 4.1.2 检索逻辑
```python
def retrieve_knowledge(hero_name, option_hexes):
    relevant = []
    for hex_id in option_hexes:
        hex_data = knowledge_base[hex_id]
        if hero_name in hex_data["synergy"]["heroes"]:
            relevant.append(hex_data)
    return relevant
```

### 4.2 完整版：ChromaDB 向量库

#### 4.2.1 数据建模
- **文档粒度**：每个海克斯一条文档
- **向量化**：使用 `text-embedding-3-small`
- **元数据**：
  ```python
  metadata = {
      "hex_id": "cybernetic_shell",
      "category": "defense",
      "hero_tags": ["tank", "fighter"],
      "priority": "A"
  }
  ```

#### 4.2.2 协同建模 (Knowledge Graph Lite)
```
[英雄] --适配--> [强化]
[强化] --协同--> [强化]
[强化] --冲突--> [强化]
```

---

## 第 5 章：决策层详细设计 (Reasoning & Persona)

### 5.1 人格化推理引擎 (Persona Engineering)

#### 5.1.1 人设注入
```python
SYSTEM_PROMPT = """
你是一名来自祖安的海克斯大乱斗教练，说话风格：
- 极度自信，从不说"建议"、"可能"、"或许"等弱词
- 用祖安俚语（如"艹"、"老子"、"给爷冲"）
- 逆风时压力山大，顺风时阴阳怪气
- 指令式短句（如"选义体！"而非"我建议选择义体外壳"）

约束：
- 回复必须在 20 字以内
- 必须包含选择理由
"""
```

#### 5.1.2 动态毒性调节 (Toxicity Scaling)
```python
def adjust_tone(kda_ratio):
    if kda_ratio > 3.0:
        return "阴阳怪气模式"  # "就这？还要我教？"
    elif kda_ratio < 0.5:
        return "压力山大模式"  # "选错直接15了！"
    else:
        return "正常指导模式"
```

### 5.2 链式思考 (Chain-of-Thought)

#### 5.2.1 推理步骤
```
Step 1: Identify (局势分析)
  - 当前英雄特性（战士/法师/坦克？）
  - 已有强化的协同方向（AP流/AD流/坦度流？）
  - KDA 表现（优势/劣势？）

Step 2: Synergize (协同计算)
  for each option in [选项1, 选项2, 选项3]:
      score = 基础分 + 英雄适配分 + 协同分 - 冲突分

Step 3: Execute (输出决策)
  - 选择最高分项
  - 生成一句话理由
  - 应用人格化风格
```

---

## 第 6 章：交互层详细设计 (Interaction Layer)

### 6.1 交互分发策略

#### 6.1.1 语音"神谕" (Audio)
- **技术**：Edge-TTS 异步合成
- **语音选择**：`zh-CN-XiaoxiaoNeural`（女声）或 `zh-CN-YunxiNeural`（男声）
- **延迟优化**：
  - 预先合成常用短语
  - 流式播放（边合成边播）
- **触发时机**：用户按键（如 F9）后 1.2s 内

#### 6.1.2 手机"第二屏" (Push)
- **工具**：Bark / PushDeer Webhook
- **推送内容**：
  ```
  【海克斯选择】
  推荐：义体外壳
  理由：你现在 0/5，选个硬的保命
  备选：再生光环（次优）
  避免：狂战士之怒（脆皮白给）
  ```
- **触发场景**：仅在复杂决策时推送（简单情况只语音）

### 6.2 状态机管理 (FSM)

```
[待机] --检测到选择界面--> [识别中]
[识别中] --识别完成--> [决策中]
[决策中] --LLM响应--> [播报中]
[播报中] --播报完成--> [待机]
```

---

## 第 7 章：工程化运维与评估 (Engineering & Evaluation)

### 7.1 容器化部署

#### 7.1.1 Docker Compose 配置
```yaml
version: '3.8'
services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data/chroma:/chroma/chroma

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  decision-agent:
    build: ./services/decision
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - CHROMA_HOST=chromadb
    depends_on:
      - chromadb
      - redis
```

### 7.2 性能评测体系 (Benchmark)

#### 7.2.1 测试集构建
- **规模**：50 组真实游戏场景
- **维度**：
  - 英雄类型覆盖（战士/法师/射手/坦克/辅助）
  - 局势差异（优势/均势/劣势）
  - 强化复杂度（纯AD流/混合流/特殊流派）

#### 7.2.2 评估指标

| 指标 | MVP 目标 | 完整版目标 |
|-----|---------|-----------|
| **识别准确率** | > 90% | > 95% |
| **推理延迟** | < 2.0s | < 1.5s |
| **人格对齐度** | 主观评分 > 7/10 | 主观评分 > 8/10 |
| **实战胜率提升** | +5% | +10% |

---

## 第 8 章：开发环境配置 (Development Setup)

### 8.1 混合开发方案

#### 8.1.1 设计原则
- **Windows 为主**：游戏环境 + 开发环境
- **服务器为辅**：Git 仓库 + 备份 + 未来部署

#### 8.1.2 环境拓扑
```
┌─────────────────────────────────────┐
│ Windows 游戏机 (开发 + 运行)          │
│ ├── Python 3.10+                    │
│ ├── Git (连接到服务器仓库)            │
│ ├── VSCode                          │
│ └── hex-strategist/                 │
│     ├── capture.py                  │
│     ├── recognize.py                │
│     ├── decision.py                 │
│     ├── main.py                     │
│     └── test_images/                │
└─────────────────────────────────────┘
         │ Git Push/Pull
         ↓
┌─────────────────────────────────────┐
│ Ubuntu 服务器 (192.168.1.200)       │
│ └── ~/projects/hex-strategist.git   │
│     (Bare Git 仓库，自动同步)         │
└─────────────────────────────────────┘
```

### 8.2 Git 工作流

#### 8.2.1 服务器初始化
```bash
# Ubuntu 服务器
mkdir -p ~/projects
cd ~/projects
git init --bare hex-strategist.git
```

#### 8.2.2 Windows 克隆
```bash
# Windows PowerShell
git clone ezreau@192.168.1.200:~/projects/hex-strategist.git
cd hex-strategist
```

#### 8.2.3 日常工作流
```bash
# 1. 开发
git add .
git commit -m "实现海克斯识别模块"

# 2. 备份到服务器
git push origin main

# 3. 服务器同步（如需部署测试）
# 在服务器上 clone 非 bare 仓库
git clone ~/projects/hex-strategist.git ~/projects/hex-strategist-deploy
```

---

## 第 9 章：数据采集策略 (Data Acquisition)

### 9.1 海克斯图标采集

#### 9.1.1 数据源
- **官方 API**：Riot Data Dragon
  - URL: `https://ddragon.leagueoflegends.com/cdn/{version}/data/zh_CN/champion.json`
  - 限制：可能不包含大乱斗专属强化

- **Wiki 爬取**：
  - 目标站点：`https://leagueoflegends.fandom.com/wiki/Arena`
  - 方法：手动下载图标 + 复制文本说明（无需写爬虫）

#### 9.1.2 MVP 采集方案（手动）
1. 打开 Wiki 页面
2. 右键保存图标到 `/assets/hex_icons/{hex_id}.png`
3. 手动创建 `hex_metadata.json`：
   ```json
   {
     "cybernetic_shell": {
       "name": "义体外壳",
       "description": "受到伤害时获得护盾"
     }
   }
   ```

### 9.2 知识库构建

#### 9.2.1 优先级分层
- **P0（必须）**：50 个高频海克斯（覆盖 80% 场景）
- **P1（补充）**：100 个中频海克斯
- **P2（完整）**：全部 200+ 海克斯

#### 9.2.2 人工标注模板
```json
{
  "hex_id": "infinity_force",
  "name": "无尽之力",
  "priority": "S",
  "good_for": ["战士", "刺客"],
  "synergy_with": ["狂战士之怒", "血手"],
  "when_to_pick": "有AD伤害且缺爆发时",
  "avoid_when": "纯坦克或法师"
}
```

---

## 第 10 章：风险与应对 (Risks & Mitigation)

### 10.1 技术风险

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| **游戏更新导致界面变化** | 识别失效 | 高 | 建立多版本 ROI 配置，添加自动检测机制 |
| **pHash 误识别率高** | 决策错误 | 中 | 引入二次确认（OCR文本匹配） |
| **LLM 响应延迟 > 2s** | 用户体验差 | 中 | 启用本地缓存 + 流式输出 |
| **API 限流** | 服务中断 | 低 | 多 API 轮询 + 降级到规则引擎 |

### 10.2 开发节奏风险

| 风险 | 应对 |
|-----|------|
| **开发进度停滞** | 灵活调整任务，专注核心功能 |
| **卡在某个技术点** | 寻求社区帮助（GitHub Issues / Reddit） |
| **家庭事务影响** | 调整开发节奏，保持持续性 |

---

## 第 11 章：面试叙事脚本 (Interview Narrative)

### 11.1 项目亮点提炼

#### 技术深度
- **计算机视觉**：pHash 指纹匹配 + OCR 混合识别
- **AI 工程化**：Prompt 工程 + 多模型对比测试
- **系统设计**：从单机到分布式的架构演进

#### 工程能力
- **快速迭代**：1 个月交付 MVP
- **性能优化**：ROI 裁剪 + 缓存策略，延迟 < 1.5s
- **可维护性**：模块化设计 + Docker 部署

### 11.2 STAR 面试话术

#### Situation
"在学习 AI Agent 开发过程中，我希望通过一个实战项目展示能力，选择了《英雄联盟》海克斯大乱斗这个高随机性场景。"

#### Task
"需要在 1 个月内实现一个能实时识别游戏画面、调用 LLM 给出决策建议、并通过语音反馈的完整系统。"

#### Action
"采用分阶段策略：
1. Week 1-2 搞定视觉识别（pHash + OCR）
2. Week 3 构建知识库和 Prompt 工程
3. Week 4 整合所有模块并优化延迟

关键技术选择：
- 用 pHash 而非深度学习，避免过度复杂
- 用 JSON 而非向量库，快速验证可行性
- 边玩边测试，确保真实场景可用"

#### Result
"最终实现了 < 2s 的端到端决策延迟，识别准确率 > 90%，并为后续升级到分布式架构留下了清晰的演进路径。"

---

## 第 12 章：后续迭代方向 (Future Roadmap)

### 12.1 功能扩展
- [ ] 敌方阵容分析（识别对面英雄 + 给出针对建议）
- [ ] 出装路线推荐（基于海克斯动态调整）
- [ ] 战局复盘（保存识别日志 + 生成分析报告）

### 12.2 技术升级
- [ ] 引入强化学习（根据历史胜率优化推荐策略）
- [ ] 多模态融合（结合小地图信息、技能冷却）
- [ ] 移动端 App（手机控制 + 实时推送）

### 12.3 社区化
- [ ] 开源到 GitHub
- [ ] 录制教学视频（B站/YouTube）
- [ ] 发布到 Reddit/NGA 收集反馈

---

## 附录 A：技术栈清单

### MVP 阶段
| 类别 | 技术 | 用途 |
|-----|------|------|
| **语言** | Python 3.10+ | 主开发语言 |
| **截屏** | mss | 高性能屏幕捕获 |
| **图像处理** | Pillow, imagehash | pHash 计算 |
| **OCR** | PaddleOCR | 文本识别 |
| **LLM** | OpenAI SDK / Anthropic SDK | API 调用 |
| **语音** | Edge-TTS | 文本转语音 |
| **数据** | JSON | 知识库存储 |

### 完整版阶段
| 类别 | 技术 | 用途 |
|-----|------|------|
| **后端框架** | FastAPI | 微服务 API |
| **向量库** | ChromaDB | 语义检索 |
| **状态管理** | Redis | FSM + 缓存 |
| **部署** | Docker Compose | 容器编排 |
| **监控** | Prometheus + Grafana | 性能监控 |
| **推送** | Bark / PushDeer | 移动端通知 |

---

## 附录 B：参考资料

### 官方文档
- [Riot Games API](https://developer.riotgames.com/)
- [Data Dragon](https://ddragon.leagueoflegends.com/)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

### 社区资源
- [英雄联盟 Wiki](https://leagueoflegends.fandom.com/wiki/Arena)
- [Reddit r/leagueoflegends](https://www.reddit.com/r/leagueoflegends/)
- [NGA 论坛](https://bbs.nga.cn/)

### 技术博客
- [pHash 原理详解](https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## 附录 C：开发日志模板

```markdown
## Week X - Day Y (YYYY-MM-DD)

### 今日目标
- [ ] 任务1
- [ ] 任务2

### 实际完成
- [x] 任务1
  - 遇到问题：XXX
  - 解决方案：XXX
- [ ] 任务2（未完成，原因：XXX）

### 明日计划
- [ ] 继续任务2
- [ ] 开始任务3

### 学习记录
- 学到的新知识：XXX
- 参考的资料：[链接]
```

---

**文档版本**：v2.0
**最后更新**：2025-12-27
**作者**：Ezreau
**项目代号**：Hex-Strategist
**目标交付日期**：2026-02-27 (MVP) / 2026-03-27 (完整版)
