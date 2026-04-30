---
name: 项目初始化规范
description: 新项目从零开始的标准化创建流程、模板选择、环境搭建 — 每次创建新项目时自动适用
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 项目初始化规范

## 触发条件
- 用户要求"创建新项目"、"开始一个项目"、"搭建一个新服务"
- 在 `/root/project/` 下创建新目录

## 初始化流程

### 1. 需求确认
- 项目名称、目标、核心功能（一句话）
- 语言/技术栈选择
- 是否需要 Docker 化
- 是否需要数据库/外部依赖

### 2. 目录脚手架
```bash
mkdir -p /root/project/<name>/{src,tests,docs,scripts}
touch /root/project/<name>/README.md
```

### 3. 环境搭建
- **Python**：创建 `requirements.txt`，激活 `/root/myenv/` 或创建项目专用 venv
- **Node**：`npm init` + 安装依赖
- **Go**：`go mod init`
- **Docker**：创建 `Dockerfile` + `.dockerignore`
- **Git**：`git init` + 创建 `.gitignore`

### 4. 基础文件模板
按 module-standards.md 创建首个模块文件，包含完整的 `__main__` 自测块

### 5. 首次验证
- 语言环境：编译/解释通过
- 首个模块：自测通过
- Docker 构建（若适用）：build 成功

## 必须创建的初始文件

| 文件 | 必要性 | 用途 |
|------|--------|------|
| `README.md` | 必须 | 项目说明、启动方式 |
| `.gitignore` | 必须 | 排除生成文件、依赖、密钥 |
| `requirements.txt` / `package.json` / `go.mod` | 必须 | 依赖声明 |
| `src/` 首个模块 | 必须 | 含自测块 |
| `tests/` 目录 | 推荐 | 集成测试 |
| `Dockerfile` | 若容器化 | 容器构建 |
| `docker-compose.yml` | 若多服务 | 编排 |
| `.env.example` | 若有密钥 | 示例配置 |

## `.gitignore` 基准内容
```
# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# Node
node_modules/
dist/
.env

# Go
*.exe
*.test
vendor/

# General
.DS_Store
*.log
*.tmp
.idea/
.vscode/
```

## 禁止
- 不创建未要求的功能模块（YAGNI）
- 不引入未确认需要的第三方依赖
- 不创建空的预留目录
- 不在初始化阶段设计"未来架构"
