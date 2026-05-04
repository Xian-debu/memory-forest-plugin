---
id: PROJECTS-BRANCH-0001
type: LEAF
tree: projects
layer: L2
status: COMPLETED
parent: PROJ-ROOT-0000
children: []
created: '2026-05-01'
completed: '2026-05-01'
heartbeat: '2026-05-01'
priority: HIGH
owner: claude-code
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
tags:
- n8n
- deepseek
- workflow
- automation
- ai-cli
- webhook
- api
experience_refs:
- EXP-PAT-0006
- EXP-PAT-0007
- EXP-PAT-0008
---

# n8n工作流系统搭建

## 目标
使用 Docker n8n 镜像和 DeepSeek API 搭建自动化工作流系统。

## 当前状态
已完成。4个活跃的 n8n 定时工作流，1个 AI CLI 工具，1个 AI Webhook 服务器。

## 关键决策

### 为什么选择混合架构
1. **n8n Webhook 受限**: n8n v1.118.2 通过纯 API 管理时 webhook 注册不工作，需要 `N8N_HOST` + `WEBHOOK_URL` 环境变量，且激活后仍不注册。Cron 触发器工作正常。
2. **Python AI CLI**: 交互式 AI 任务（chat/review/summarize/translate）通过 stdlib 实现的 CLI 工具，零依赖，直接调用 DeepSeek API。
3. **Python Webhook Server**: 弥补 n8n webhook 不足，提供 RESTful API 端点。
4. **n8n 定时任务**: Daily AI Digest, Weekly Report, Dev Tip of the Day 使用 Cron 触发器自动运行。

### 技术选型
- **DeepSeek API**: Anthropic-compatible endpoint (api.deepseek.com/anthropic)，支持 Claude 模型命名
- **DeepSeek V4 特性**: 返回 thinking + text 两个 content block，thinking 消耗大量 tokens
- **n8n Docker**: n8nio/n8n:latest，Python 3 stdlib 实现 webhook server（PEP 668 阻止 pip install）
- **Cookie 认证**: Netscape cookie 格式，HttpOnly 标记需特殊解析

### n8n 环境配置
```
N8N_HOST=localhost
WEBHOOK_URL=http://localhost:5678
N8N_SECURE_COOKIE=false
```

## 交付物

### AI CLI (`/root/.claude/scripts/ai_cli.py`)
- `ai chat` — 交互式 AI 对话
- `ai review` — 代码审查（bugs/security/perf/style）
- `ai summarize` — 文本摘要
- `ai translate <lang>` — 翻译

### AI Webhook Server (`/root/.claude/scripts/ai_webhook_server.py`)
- 端口 8899，零依赖 stdlib 实现
- 端点: /chat /review /summarize /translate /health /help

### n8n 定时工作流（4个活跃）
1. **Daily AI Digest** (每日 8:00) — AI 生成开发趋势摘要
2. **Weekly Memory Forest Report** (周日 9:00) — 周项目状态报告
3. **AI Dev Tip of the Day** (每日 8:30) — 实用开发者技巧
4. **Data Pipeline Demo** (手动触发) — 多主题 API 编排演示

### n8n Manager CLI (`/root/.claude/scripts/n8n_manager.py`)
- `n8nls` — 列出工作流
- `n8nstat` — 状态概览
- 凭据: admin@local.dev / Admin123!

### Shell 别名
ai, aichat, aireview, aisum, aitrans, aiserve, n8nw, n8nls, n8nstat

## 经验提炼
- [EXP-PAT-0006](experiences-tree/patterns/n8n-webhook-registration.md) — n8n Webhook 注册的环境依赖
- [EXP-PAT-0007](experiences-tree/patterns/deepseek-thinking-block.md) — DeepSeek V4 thinking block 的 token 消耗
- [EXP-PAT-0008](experiences-tree/patterns/hybrid-architecture-fallback.md) — 混合架构回退策略
