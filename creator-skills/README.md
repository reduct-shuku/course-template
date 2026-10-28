# 课程创作工具集

本目录集中所有帮助创作者设计、实现、改进和验证课程网页的能力。

| 位置 | 作用 |
|---|---|
| SKILL.md | 创作规范总入口 |
| guides/、references/ | 专项指南与教学/视觉参考 |
| evals/scenarios.json | 创作、修改、修复、准备和上传边界的回归审阅场景 |
| preferences/ | 已确认的创作偏好 |
| shared/ | 公共组件、设计系统、公式、图表和 SceneDeck |
| tools/content/、tools/checks/ | 内容生成与页面检查工具 |
| tools/python/idl_authoring/ | Python 内容、媒体和模型准备工具 |
| tools/python/idl_authoring/identity.py、keys.py | 新课程身份签发、验证与密钥初始化 |
| check.ps1、tests/ | 统一构建、测试和身份验证 |
| demos/ | 创作参考与独立 Web Agent 演示 |
| integration/ | 可选自动化接入描述 |

公共组件通过 @shared/react 导入；依赖仍由 environment/ 安装，预览由 runtime/start.ps1 启动。组件被网页运行时引用，不改变它作为创作工具的归属。

从项目根目录执行 `./creator-skills/check.ps1`；-Kind backend / agent-demo / all 选择对应验证。完整用法见 [根目录说明](../README.md)。

本轮规范参考 [intuitive-deep-learning develop 的 creator-skill](https://github.com/ReductTech/intuitive-deep-learning/tree/cc204d4843f8ac484f63695139ab76cc17dc0c9e/creator-skill)，将教学设计、大纲、实现和验收拆为按需指南。路径、身份签名和上传约定以本模板为准；没有复制参考课程或原作者个人偏好。
