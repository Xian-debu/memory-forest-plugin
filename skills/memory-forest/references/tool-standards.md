---
name: 工具调用规范
description: Claude Code 工具选择决策树、并行化规则、权限边界 — 每次工具调用时自动适用
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 工具调用规范

## 工具选择决策树

```
读文件        → Read（非 cat/head/tail）
写新文件      → Write（非 echo/cat <<EOF）
编辑已有文件  → Edit（非 sed/awk）
搜索代码      → Bash: grep/find（非 Agent Explore，除非 > 3 次搜索）
目录浏览      → Bash: ls/tree
git 操作      → Bash: git 命令
GitHub 操作   → Bash: gh 命令
系统命令      → Bash
网页抓取      → WebFetch
网页搜索      → WebSearch
多步探索      → Agent(subagent_type="Explore")
复杂实现      → Agent(subagent_type="general-purpose")
架构规划      → Agent(subagent_type="Plan")
用户问答      → AskUserQuestion
```

## 并行化规则
- **独立调用必须并行**：多个工具调用之间无数据依赖时，在同一条消息中并发发送
- **依赖调用串行**：后续调用依赖前一个调用结果时，必须等待前一个完成
- **批量文件读取**：需要读取多个文件时，一次发送所有 Read 调用
- **批量文件写入**：创建多个不相关的文件时，一次发送所有 Write 调用
- **git 命令**：`git status`、`git diff`、`git log` 可同时发送

## 权限边界
- root 权限环境下，工具调用无系统级限制
- 但以下操作必须征求用户确认：
  - `rm -rf` 类删除操作
  - `git reset --hard` / `git push --force`
  - `docker rm -f` 容器强制删除
  - 修改 `/etc/` 系统配置
  - 安装系统级软件包（apt install）
  - 修改 `.claude/` 配置目录外的任何隐藏文件

## Bash 调用规范
- 命令描述（description 参数）用英文，简短（5-10 词），动词开头
- 使用绝对路径，不依赖 `cd` 改变的工作目录
- 长运行命令（编译、安装）使用 `run_in_background: true` 或设置较长 timeout
- 链式命令用 `&&`，仅在无需关注中间失败时用 `;`
- **绝不**在 Bash 中做 `cat file | grep` 的事 — 用 Read + Grep

## Edit 调用规范
- `old_string` 必须精确匹配（包括缩进），取自 Read 结果
- 若匹配不唯一，扩大上下文使其唯一，或使用 `replace_all`
- 一次 Edit 只改一处逻辑；多处理解为多个 Edit 调用
- 修改前必须 Read 过该文件（即使之前读过）

## 常见错误避免
- [ ] 不用 `cat` 读文件 → 用 Read
- [ ] 不用 `echo` 写文件 → 用 Write
- [ ] 不用 `sed -i` 改文件 → 用 Edit
- [ ] 不用 `find /` 扫描全盘 → 限定搜索根路径
- [ ] 不在一句消息中既问用户又调用工具 → 先调用再问
