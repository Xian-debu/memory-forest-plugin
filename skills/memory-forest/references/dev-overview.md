---
name: 开发总述
description: 此环境下的开发总体原则、环境配置、项目结构约定
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 开发总述

## 环境画像
- **系统**：WSL2 Ubuntu 24.04.3 LTS, x86_64
- **权限**：root（无限制）
- **Python**：3.12.3，虚拟环境 `/root/myenv/`（系统级包 + venv 隔离）
- **Node**：v22.21.1（nvm 管理），全局安装有 Claude Code CLI
- **Docker**：28.3.2（开机自启），可用于容器化开发与测试
- **编译器**：GCC 13.3.0 / G++ 13.3.0
- **已有项目**：`/root/project/`（MQTT 服务端 + 客户端）

## 开发首要原则
1. **安全第一**：即使有 root 权限，也需遵循最小权限原则。不写入系统关键路径，不修改 /etc 除非明确需要
2. **Plan-then-Code**：任何非平凡任务必须使用 EnterPlanMode 先规划，获得用户确认后再实现
3. **最小变更**：修改集中于目标文件，不做无关重构、格式化、import 整理
4. **可验证性**：每次修改后必须提供可验证的证据（运行结果、测试输出）
5. **破坏性操作必确认**：rm -rf、git reset --hard、docker rm -f、数据库删除等操作必须先征求用户确认

## 项目目录约定
```
/root/project/<project-name>/
├── src/             # 源代码
├── tests/           # 测试代码
├── docs/            # 项目文档
├── scripts/         # 构建/部署脚本
├── Dockerfile       # 若容器化
├── requirements.txt # Python 依赖
└── README.md        # 项目说明
```

## 语言选择优先级
- **系统工具/CLI**：Python（快速开发）
- **高性能服务**：Go 或 C/C++
- **Web 前端**：TypeScript + React
- **脚本/胶水**：Bash（简单场景）或 Python（复杂逻辑）

## 环境变量与配置
- 生产密钥不写入代码，使用环境变量或 `.env` 文件
- `.env` 文件加入 `.gitignore`
- 示例配置写入 `.env.example`

## 与 Claude Code 的关系
- Claude Code 是该环境的**开发执行引擎**
- 所有代码产出由 Claude Code 直接编写、测试、验证
- 用户提供需求和决策，Claude Code 负责实现和自检
