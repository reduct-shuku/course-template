# 课程创作工具集

本目录集中所有帮助创作者设计、实现、改进和验证课程网页的能力。

| 位置 | 作用 |
|---|---|
| SKILL.md | 创作规范总入口 |
| guides/、references/ | 专项指南与教学/视觉参考 |
| preferences/ | 已确认的创作偏好 |
| shared/ | 公共组件、设计系统、公式、图表和 SceneDeck |
| tools/content/、tools/checks/ | 内容生成与页面检查工具 |
| tools/python/idl_authoring/ | Python 内容、媒体和模型准备工具 |
| tools/python/idl_authoring/identity.py、keys.py | 新课程身份签发、验证与密钥初始化 |
| check.ps1、tests/ | 统一构建、测试和身份验证 |
| demos/ | 创作参考与独立 Web Agent 演示 |
| integration/ | 可选自动化接入描述 |

公共组件通过 @shared/react 导入；依赖仍由 environment/ 安装，预览由 runtime/start.ps1 启动。组件被网页运行时引用，不改变它作为创作工具的归属。

从项目根目录执行 `./creater-skills/check.ps1`；-Kind backend / agent-demo / all 选择对应验证。完整用法见 [根目录说明](../README.md)。
