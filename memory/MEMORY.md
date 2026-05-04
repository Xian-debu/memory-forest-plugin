# 记忆森林 — 入口索引

## 森林入口（最高优先级，先于一切）
- [广义指导思想](PHILOSOPHY.md) — **L5 绝对底层哲学根**，会话启动第一加载，一切规范之源头
- [记忆森林根源](forest-root.md) — 记忆管理框架入口，受哲学层约束
- [记忆森林规范](MF-SPEC.md) — 森林架构、节点类型、分层、心跳、垃圾回收
- [记忆森林运行时](MF-RUNTIME.md) — 会话生命周期、加载决策树、防溢出机制

## 记忆树索引

### system-tree — 系统配置
- [系统树根](system-tree/ROOT.md) — 所有开发规范、方法论、安全边界的集合
- [核心配置分支](system-tree/branch-config.md) — 角色定义 + 环境画像
- [方法论分支](system-tree/branch-methodology.md) — 技术方法论 + 调试 + 设计
- [质量标准分支](system-tree/branch-quality.md) — 开发/文档/模块/工具/自检/验证
- [安全分支](system-tree/branch-safety.md) — 系统操作安全边界
- [元规范分支](system-tree/branch-meta.md) — 文档引导/关系/修订/项目初始化

### experiences-tree — 核心经验
- [经验池根](experiences-tree/ROOT.md) — L3 跨项目模式 + L4 核心原则

### projects-tree — 项目记忆
- [项目树根](projects-tree/ROOT.md) — 所有项目任务记忆的集合
- [框架重构](projects-tree/framework-refactor/ROOT.md) — 实验框架模块化重构 (Phase 1-11 完成, 31 模块 + 16 模型 + 批量无人值守 + networks/ 目录 + --skip-load 缓存)
- [ATFF-Net](projects-tree/framework-refactor/leaf-atff-net.md) — 可学习 Gabor 滤波器组 + 跨频带注意力 + 多尺度扩张卷积 (~56K)
- [Hawk-II](projects-tree/framework-refactor/leaf-hawk2.md) — 多域多尺度特征提取 + GPU XGBoost + CUDA 兼容性修复 (Hilbert 包络, ~335d)
- [首次自我进化](projects-tree/evolution-1-self-evolution.md) — Stop Hook + mf CLI + MCP Server + SessionStart + 权限优化 (2026-05-01 完成)

### projects-tree — 项目记忆 (续)
- [n8n工作流系统](projects-tree/PROJECTS-BRANCH-0001.md) — n8n Docker + DeepSeek API + AI CLI + Webhook Server (2026-05-01 完成)

### 自动化基础设施
- [核心库](/.claude/scripts/memory_forest.py) — 记忆森林 Python 核心库 (frontmatter 解析, 心跳, GC, 搜索, 健康检查)
- [CLI 工具](/.claude/scripts/mf.py) — mf 命令行工具 (status/heartbeat/gc/search/health/create/list/show)
- [MCP Server](/.claude/scripts/mcp_memory_forest.py) — MCP 协议服务 (8 个工具, JSON-RPC 2.0 over stdio)
- [Stop Hook](/.claude/scripts/heartbeat_hook.py) — 会话退出自动心跳
- [SessionStart Hook](/.claude/scripts/startup_hook.py) — 会话启动自检
- [AI CLI](/.claude/scripts/ai_cli.py) — 交互式 AI 工具 (chat/review/summarize/translate, DeepSeek API)
- [AI Webhook Server](/.claude/scripts/ai_webhook_server.py) — AI HTTP API 服务 (5 个端点, 零依赖)
- [n8n Manager](/.claude/scripts/n8n_manager.py) — n8n 工作流管理器 (list/show/toggle/create)
- [AI 服务启动脚本](/.claude/scripts/start_ai_services.sh) — 一键启动 n8n + AI Webhook Server
- [工作流别名](/.claude/scripts/aliases.sh) — mf/docker/claude/n8n/ai 快捷命令

## 加载顺序（不可变）
```
PHILOSOPHY → forest-root → MF-SPEC → MF-RUNTIME → system-tree → (当前项目树)
```
然后加载自动化脚本: SessionStart hook → mf status → (工作) → Stop hook

**PHILOSOPHY.md 位于 L5 绝对底层，是一切规范、配置、经验的最终约束。任何下层与哲学层冲突时，哲学层胜出。**
