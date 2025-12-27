# Project Hex-Strategist: 深度演训白皮书
## 基于多模态 RAG、实时视觉感知与人格化 Agent 的英雄联盟"海克斯大乱斗"决策系统

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

### 0.5.4 时间预算
| 时间维度 | 可用时间 |
|---------|---------|
| 周一/三/五 | 3小时/天 (18:30-24:30，扣除3h家庭时间) |
| 周二/四 | 2小时/天 (21:30-24:30，扣除1h家庭时间) |
| 周六/日 | 2小时/天 (22:30-24:30) |
| **每周总计** | **17小时** |
| **每月总计** | **68小时** |

### 0.5.5 项目周期
- **MVP 目标**：1个月（68小时）
- **完整版目标**：2个月（136小时）

---

## 第 0.6 章：双阶段架构策略 (Two-Phase Architecture)

### 设计哲学：先跑通，再优化

```
Phase 1: MVP 单机版          Phase 2: 分布式完整版
   (Month 1)          →          (Month 2)
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

## 第 1 章：MVP 开发计划 (4-Week Roadmap)

### Week 1: 感知层 - "让程序看到游戏"
**目标**：实现稳定的游戏画面采集与基础OCR

#### 任务清单
- [ ] **环境搭建** (6小时)
  - Windows 安装 Python 3.10+
  - 配置 Git 与服务器仓库连接
  - 安装 VSCode + Python 插件

- [ ] **截屏模块** (4小时)
  - 使用 `mss` 库实现全屏截图
  - 测试不同分辨率下的性能
  - 记录帧率影响数据

- [ ] **ROI 裁剪** (3小时)
  - 打5局游戏，记录海克斯选择界面的固定坐标
  - 实现动态 ROI 提取（仅处理关键区域）
  - 验证不同分辨率的适配性

- [ ] **基础 OCR** (4小时)
  - 集成 PaddleOCR
  - 识别英雄名称、KDA、金币
  - 建立测试截图库（20张+）

**交付物**：
- `capture.py` - 截屏与ROI裁剪
- `ocr_test.py` - OCR识别测试脚本
- `/test_images/` - 测试截图库

---

### Week 2: 识别层 - "让程序认出海克斯"
**目标**：建立海克斯图标识别系统

#### 任务清单
- [ ] **数据采集** (5小时)
  - 从 Wiki/DataDragon 下载海克斯图标（200+）
  - 手动分类：攻击、法术、防御、辅助、传说
  - 建立图标ID与名称的映射表

- [ ] **pHash 指纹库** (6小时)
  - 为每个图标计算 pHash 值
  - 存储为 `hex_fingerprints.json`
  - 实现指纹比对函数（汉明距离）

- [ ] **识别测试** (4小时)
  - 在实际截图上测试识别准确率
  - 调整相似度阈值
  - 处理边缘情况（图标被遮挡、光效干扰）

- [ ] **性能优化** (2小时)
  - 确保单次识别 < 100ms
  - 使用缓存避免重复计算

**交付物**：
- `recognize.py` - pHash 匹配引擎
- `hex_fingerprints.json` - 图标指纹库
- `hex_metadata.json` - 图标元数据（名称、类别、简介）

---

### Week 3: 决策层 - "让 AI 给建议"
**目标**：实现基于 LLM 的决策推理

#### 任务清单
- [ ] **知识库构建** (8小时)
  - 手动整理 50 个常见海克斯的机制说明
  - 为每个海克斯标注：
    - 适用英雄类型（战士/法师/射手/坦克/辅助）
    - 协同强化（与哪些强化配合好）
    - 优先级（S/A/B/C/D）
  - 存储为 `knowledge_base.json`

- [ ] **Prompt 工程** (5小时)
  - 设计系统提示词（角色定位："祖安毒舌教练"）
  - 设计决策提示词模板：
    ```
    当前英雄: {hero_name}
    已有强化: {existing_hexes}
    可选强化: {option_1}, {option_2}, {option_3}
    相关知识: {retrieved_knowledge}

    任务: 选出最优项，用一句话说明理由（禁止使用"建议"等弱语气词）
    ```
  - 测试 3 种模型的输出质量（Gemini/Claude/DeepSeek）

- [ ] **API 调用模块** (4小时)
  - 封装 LLM API 调用逻辑
  - 实现错误重试机制
  - 记录调用日志（Prompt + Response）

**交付物**：
- `knowledge_base.json` - 海克斯知识库
- `decision.py` - 决策推理模块
- `prompts.py` - Prompt 模板管理

---

### Week 4: 整合 - "能用了"
**目标**：串联所有模块，实现完整流程

#### 任务清单
- [ ] **主流程编排** (6小时)
  - 实现 `main.py` 主循环
  - 状态机：待机 → 检测选择界面 → 识别 → 决策 → 播报
  - 添加快捷键触发（如按 F9 开始识别）

- [ ] **语音输出** (4小时)
  - 集成 Edge-TTS
  - 选择合适的中文语音（如 "晓晓"）
  - 优化延迟（异步合成 + 播放）

- [ ] **测试与调试** (5小时)
  - 进行 10 局实战测试
  - 记录问题：误识别、延迟、崩溃
  - 修复关键 Bug

- [ ] **文档与演示** (2小时)
  - 编写 README.md
  - 录制演示视频（3分钟）
  - 准备面试讲解脚本

**交付物**：
- `main.py` - 主程序入口
- `tts.py` - 语音播报模块
- `README.md` - 项目文档
- `demo.mp4` - 演示视频

---

## 第 2 章：完整版系统架构设计 (Full-Scale Architecture)

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

### 10.2 时间风险

| 风险 | 应对 |
|-----|------|
| **某周开发时间不足** | 预留 Week 4 的 2 天作为缓冲 |
| **卡在某个技术点** | 寻求社区帮助（GitHub Issues / Reddit） |
| **家庭事务突发** | 延长 MVP 周期到 5 周（可接受） |

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
