# 环境安装与配置

从项目根目录执行 `./environment/install.ps1`，默认只安装课程前端。

| Kind | 安装内容 |
|---|---|
| frontend（默认） | environment/frontend/package-lock.json 锁定的 npm 依赖 |
| backend | environment/backend/.venv 和 Python 后端、工具、测试依赖 |
| agent-demo | environment/agent-demo/ 的独立演示 npm 依赖 |
| all | 上述三项 |

后端要求 Python 3.10+；通过 -Python 或 IDL_PYTHON 指定解释器。Torch / torchvision 需按 CPU/CUDA 平台单独安装。

前端与演示各有 package.json、锁文件、tsconfig.json 和 vite.config.ts；配置指向 runtime/ 下的源码。npm 命令必须带 `--prefix environment/frontend` 或 `--prefix environment/agent-demo`，或者进入对应环境目录后运行。

Python 包配置位于 environment/backend/pyproject.toml，同时安装服务包 runtime/backend/src/idl_backend/ 和创作工具包 creater-skills/tools/python/idl_authoring/。editable 安装需保留完整四目录工程：`python -m pip install -e './environment/backend[vision,assessment,dev,tools,test]'`（在项目根目录执行）。

前端配置写入 environment/frontend/.env.local；供应商密钥只使用后端环境变量或 environment/backend/settings.json。不要把密钥放进 VITE_* 配置。不要将 .venv、node_modules、settings.json、.private 或运行产物作为模板分发。

启动/停止/验证入口在 runtime/；详见 [使用说明](../README.md)。
