# Hex-Strategist

基于多模态 RAG、实时视觉感知与人格化 Agent 的英雄联盟"海克斯大乱斗"决策系统

## 项目状态

- **当前阶段**: MVP 开发中
- **目标交付**: 2026-02-27

## 快速开始

### 环境要求
- Python 3.10+
- Windows 10/11 (运行英雄联盟)

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行
```bash
python src/main.py
```

## 项目结构

```
Hex_Strategist/
├── src/                    # 源代码
│   ├── capture.py         # 截屏模块
│   ├── recognize.py       # 识别模块
│   ├── decision.py        # 决策模块
│   ├── tts.py            # 语音播报
│   └── main.py           # 主程序
├── assets/                # 资源文件
│   ├── hex_icons/        # 海克斯图标
│   └── test_images/      # 测试截图
├── data/                  # 数据文件
│   ├── knowledge_base.json
│   └── hex_fingerprints.json
├── tests/                 # 测试代码
└── docs/                  # 文档
```

## 开发计划

详见 [开发白皮书](./Project_Hex_Strategist_Whitepaper.md)

### Week 1: 感知层 (进行中)
- [ ] 环境搭建
- [ ] 截屏模块
- [ ] ROI 裁剪
- [ ] 基础 OCR

### Week 2: 识别层
- [ ] 数据采集
- [ ] pHash 指纹库
- [ ] 识别测试

### Week 3: 决策层
- [ ] 知识库构建
- [ ] Prompt 工程
- [ ] API 调用模块

### Week 4: 整合
- [ ] 主流程编排
- [ ] 语音输出
- [ ] 测试与调试

## 技术栈

- **截屏**: mss
- **OCR**: PaddleOCR
- **图像识别**: imagehash (pHash)
- **LLM**: Gemini / Claude / DeepSeek
- **语音**: Edge-TTS

## 许可证

MIT License

## 作者

Ezreau - 从制造业转行的 AI Agent 开发者
