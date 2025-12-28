# Git 快速上手指南

**适用对象**：Git 新手 / 不熟悉 Git 的开发者
**目的**：在 Hex-Strategist 项目中正确使用 Git 版本控制

---

## 📚 Git 是什么？

Git 是一个**版本控制系统**，就像游戏的"存档点"：
- 每次完成一个功能，就"保存"一个版本
- 如果代码写坏了，可以"读档"回到之前的版本
- 可以同步到服务器，防止本地文件丢失

---

## 🎯 本项目的 Git 工作流

```
你的 Windows 电脑              Ubuntu 服务器（192.168.1.200）
┌─────────────────┐            ┌─────────────────┐
│ E:\jiqixuexi\   │            │ ~/projects/     │
│ Hex_Strategist/ │   push     │ hex-strategist  │
│                 │ ─────────> │     .git        │
│   .git (本地仓库) │            │  (远程仓库)      │
└─────────────────┘            └─────────────────┘
```

**工作流程**：
1. 在 Windows 上写代码
2. 测试通过后，用 Git 提交（commit）
3. 推送（push）到服务器备份
4. 继续下一个功能

---

## 🚀 常用命令速查表

### 1️⃣ 查看状态（最常用）

```bash
git status
```

**作用**：查看哪些文件被修改了

**输出示例**：
```
On branch master
Changes not staged for commit:
  modified:   src/capture.py        # 红色 = 已修改但未添加

Untracked files:
  tests/test_capture.py             # 红色 = 新文件未跟踪
```

**💡 提示**：每次提交前先运行这个命令，确认改了哪些文件

---

### 2️⃣ 添加文件到暂存区

```bash
# 添加所有修改过的文件
git add .

# 或者只添加指定文件
git add src/capture.py
git add tests/test_capture.py
```

**作用**：告诉 Git"我要保存这些文件"

**再次查看状态**：
```bash
git status
# 现在文件应该变成绿色（已暂存）
```

---

### 3️⃣ 提交（保存版本）

```bash
git commit -m "提交说明"
```

**作用**：创建一个"存档点"

**提交说明格式建议**：
```bash
# ✅ 好的提交说明（清晰描述做了什么）
git commit -m "Implement basic screenshot functionality"
git commit -m "Add ROI configuration and test"
git commit -m "Fix pHash matching bug"

# ❌ 不好的提交说明（太模糊）
git commit -m "update"
git commit -m "fix bug"
git commit -m "aaa"
```

---

### 4️⃣ 推送到服务器（备份）

```bash
git push origin master
```

**作用**：把本地的提交同步到服务器

**可能遇到的问题**：
```bash
# 如果提示输入密码
# 输入服务器的 SSH 密码（ezreau@192.168.1.200 的密码）
```

---

### 5️⃣ 查看提交历史

```bash
# 简洁模式（推荐）
git log --oneline

# 输出示例：
# a1b2c3d Add ROI configuration
# e4f5g6h Implement screenshot
# i7j8k9l Initial commit
```

**作用**：查看所有"存档点"

---

### 6️⃣ 查看修改内容

```bash
git diff
```

**作用**：查看具体改了哪些代码（提交前检查用）

**输出示例**：
```diff
- old_code = 123
+ new_code = 456    # 绿色 + 表示新增，红色 - 表示删除
```

---

## 📋 典型工作流程（完整示例）

### 场景：完成 Step 1.1 - 实现基础截图功能

```bash
# 1. 写代码前，确认当前分支
git status
# 输出：On branch master

# 2. 写代码 + 测试（略）
# 创建了 src/capture.py
# 创建了 tests/test_capture.py

# 3. 测试通过后，查看状态
git status
# 输出：
# Untracked files:
#   src/capture.py
#   tests/test_capture.py

# 4. 添加到暂存区
git add src/capture.py tests/test_capture.py

# 5. 再次确认
git status
# 输出：
# Changes to be committed:
#   new file:   src/capture.py       # 绿色
#   new file:   tests/test_capture.py

# 6. 提交
git commit -m "Implement basic screenshot functionality"
# 输出：
# [master a1b2c3d] Implement basic screenshot functionality
#  2 files changed, 45 insertions(+)

# 7. 推送到服务器
git push origin master
# 输出：
# To ezreau@192.168.1.200:~/projects/hex-strategist.git
#    e4f5g6h..a1b2c3d  master -> master

# 8. 完成！继续下一个步骤
```

---

## ⚠️ 常见错误与解决方案

### 错误1：忘记 `git add` 就直接 `commit`

```bash
git commit -m "xxx"
# 输出：nothing to commit, working tree clean
```

**原因**：没有添加文件到暂存区

**解决**：先 `git add .`，再 `git commit`

---

### 错误2：提交说明写错了

```bash
git commit -m "这是错误的说明"
# 哎呀，打错字了！
```

**解决**：修改最后一次提交
```bash
git commit --amend -m "这是正确的说明"
```

**⚠️ 注意**：只能修改**最后一次**提交，已经 push 的不要改

---

### 错误3：不小心添加了不该提交的文件

```bash
git add .
# 哎呀，把 output/ 目录也添加进去了！
```

**解决**：从暂存区移除
```bash
git reset output/
# 或者移除所有
git reset
```

---

### 错误4：忘记提交就开始写下一个功能

**场景**：Step 1.1 做完了，忘记提交，直接开始 Step 1.2

**后果**：两个功能混在一起，无法单独回滚

**解决**：
```bash
# 先查看当前状态
git status

# 如果能分清哪些文件属于哪个步骤
git add <Step1.1的文件>
git commit -m "Step 1.1"

git add <Step1.2的文件>
git commit -m "Step 1.2"

# 如果分不清了...
# 建议：全部提交，下次注意及时提交
git add .
git commit -m "Complete Step 1.1 and 1.2"
```

**💡 预防**：**每个步骤测试通过后立即提交**

---

## 🎓 高级技巧（可选）

### 1. 查看某个文件的修改历史

```bash
git log --oneline -- src/capture.py
```

### 2. 回退到之前的版本（慎用）

```bash
# 查看历史
git log --oneline
# a1b2c3d Step 1.1
# e4f5g6h Step 0.8
# i7j8k9l Initial commit

# 回退到 Step 0.8
git reset --hard e4f5g6h

# ⚠️ 警告：这会丢失 Step 1.1 的所有代码！
```

**建议**：MVP 阶段不要用这个，写错了就修改后重新提交

### 3. 创建分支（实验功能时用）

```bash
# 创建实验分支
git branch experiment

# 切换到实验分支
git checkout experiment

# 在实验分支上随便改代码
# 如果成功了，合并回 master
git checkout master
git merge experiment

# 如果失败了，直接删除实验分支
git branch -D experiment
```

**MVP 阶段建议**：不用分支，直接在 master 上开发，简单高效

---

## 📝 本项目的提交规范

### 提交消息格式

```bash
# 功能实现
git commit -m "Implement <功能名称>"
# 示例：Implement basic screenshot functionality

# 添加测试
git commit -m "Add <测试名称>"
# 示例：Add ROI configuration and test

# 修复 Bug
git commit -m "Fix <Bug描述>"
# 示例：Fix pHash threshold issue

# 更新文档
git commit -m "Update <文档名称>"
# 示例：Update README with installation steps

# 完成某个阶段
git commit -m "Complete <阶段名称>"
# 示例：Complete Phase 1 integration test
```

### 什么时候提交？

✅ **应该提交的时机**：
1. 每个原子步骤测试通过后
2. 修复了一个 Bug 后
3. 完成一个阶段的集成测试后
4. 每天结束工作前

❌ **不应该提交的时机**：
1. 代码还没测试
2. 测试不通过
3. 代码写到一半

---

## 🛠️ 项目初始化（Step 0.3-0.4）

### 在服务器上创建仓库

```bash
# SSH 登录服务器
ssh ezreau@192.168.1.200

# 创建 bare 仓库
mkdir -p ~/projects
cd ~/projects
git init --bare hex-strategist.git

# 退出服务器
exit
```

### 在 Windows 上克隆仓库

```bash
# PowerShell
cd e:\jiqixuexi

# 克隆
git clone ezreau@192.168.1.200:~/projects/hex-strategist.git Hex_Strategist

# 进入目录
cd Hex_Strategist

# 查看状态
git status
# 输出：On branch master（或 main）
```

---

## 📖 学习资源（可选）

### 推荐教程
1. **廖雪峰 Git 教程**（中文，新手友好）
   - https://www.liaoxuefeng.com/wiki/896043488029600

2. **Git 官方文档**（英文）
   - https://git-scm.com/doc

### 图形化工具（如果命令行不习惯）
- **GitHub Desktop**（简单易用）
- **Sourcetree**（功能强大）
- **VSCode Git 插件**（编辑器集成）

**建议**：MVP 阶段用命令行，熟悉后再用图形化工具

---

## 🎯 快速检查清单

**每次提交前检查**：

- [ ] `git status` - 确认修改的文件正确
- [ ] `git diff` - 查看具体改动（可选）
- [ ] `git add .` - 添加所有文件
- [ ] `git status` - 确认暂存区（文件应该变绿）
- [ ] `git commit -m "清晰的说明"` - 提交
- [ ] `git push origin master` - 推送到服务器

**每天开始工作前**：
- [ ] `git status` - 确认工作区干净
- [ ] `git log --oneline` - 回顾昨天的进度

---

## 🆘 紧急救援

### 场景：代码写坏了，想恢复到上次提交的状态

```bash
# 放弃所有未提交的修改（慎用！）
git reset --hard HEAD

# 或者只恢复某个文件
git checkout -- src/capture.py
```

### 场景：不小心删除了文件

```bash
# 如果还没提交，可以恢复
git checkout -- <文件名>

# 如果已经提交了，从历史中找回
git log --oneline
git checkout <commit-id> -- <文件名>
```

### 场景：Push 失败

```bash
# 错误信息：Updates were rejected...

# 原因：服务器上有更新的版本
# 解决：先拉取服务器的更新
git pull origin master

# 如果有冲突，手动解决后再 push
git push origin master
```

---

## 🎓 本项目的 Git 使用建议

1. **频繁提交**：每个原子步骤测试通过就提交，不要攒着一起提交
2. **清晰说明**：提交说明要写清楚做了什么，方便回顾
3. **及时推送**：每天结束工作前推送到服务器，防止本地文件丢失
4. **不提交临时文件**：`output/`, `logs/`, `*.pyc` 等已在 `.gitignore` 中忽略
5. **测试通过再提交**：不要提交不能运行的代码

---

## 📞 需要帮助？

- 遇到 Git 错误不知道怎么办？
  - 先复制错误信息，搜索 "git 错误信息"
  - 或者保持当前状态，询问有经验的人

- 不确定是否应该提交某个文件？
  - 运行 `git status`，看看文件是什么类型
  - 源代码（`.py`）→ 提交
  - 测试文件（`tests/`）→ 提交
  - 配置文件（`.py`, `.json`）→ 提交
  - 临时输出（`output/`, `logs/`）→ 不提交

---

**记住**：Git 就是你的"存档系统"，多存档总是好的！

**最重要的三个命令**：
```bash
git add .
git commit -m "说明"
git push origin master
```

**熟练这三个，就能完成 90% 的工作！**

---

**版本**：v1.0
**更新日期**：2025-12-27
**作者**：Ezreau
