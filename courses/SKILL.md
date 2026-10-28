---
name: course-library
description: 按课程大纲引导学习，并在配套 course-template 环境中启动课程的 Guide 或 PPT 预览。适用于学习、讲授本课程库中的知识或体验教学模拟；当前包含视觉生成、GAN 和 Diffusion 课程。
---

# 互动课程库

## Shuku 版本检查

触发时先读取同目录的 [shuku.json](shuku.json)，使用 `repository`、`ref`、`path` 获取对应远程位置的最新 shuku.json，比较三段式语义版本。

- 远程版本更高：展示本地版本、远程版本和 `changes`，询问用户是否更新；经确认后才可覆盖本地文件。
- 版本一致：继续使用。远程版本更低或无法比较：使用本地版本，不自动降级。
- 仓库地址尚未配置或 GitHub 无法访问：说明未完成更新检查，继续使用本地课程。

## 学习与演示

当前目录下每个课程子目录通过 outlines.json 描述课程。先根据用户主题选择课程，再读取对应大纲，选择页面；需要阅读具体交互实现时，再读取对应 course.tsx 和页面文件。

当前课程：[视觉生成：从噪声到图像](Visual-Generation-Guide/README.md)，其 [大纲](Visual-Generation-Guide/outlines.json) 与 [页面索引](Visual-Generation-Guide/course.tsx) 覆盖生成概念、GAN 及其训练、Diffusion 的前向与反向过程，共 20 页。

开场照片是预先生成的素材，GAN 和 Diffusion 交互是浏览器内教学模拟；说明其实际能力，不把它们描述为调用真实图像生成服务或大模型训练。

## 启动互动课程

本 Skill 当前随 course-template 配套使用，页面依赖其中的 Shared、Vite 配置和统一素材目录。独立复制此模块不能直接启动网页；先检查配套文件是否存在，缺少时说明需要完整项目，不自行下载不明依赖。

在当前布局中，从本目录向上两级找到包含 `environment/install.ps1`、`runtime/start.ps1` 和 `creator-skills/shared/` 的 course-template 根目录。所有启动命令在该根目录执行：

```powershell
.\environment\install.ps1
.\runtime\start.ps1
```

依赖已安装时直接启动。状态、停止命令为 `./runtime/start.ps1 -Status`、`./runtime/stop.ps1`。

- 连续阅读：http://127.0.0.1:5173/modules/visual-generation-guide
- 课堂演示：http://127.0.0.1:5173/scenedeck/?deck=visual-generation-guide

使用启动命令实际返回的地址；若端口发生变化，同步调整链接。启动失败时查看命令输出和根目录 `runtime/data/` 下的日志。课程教学模拟不需要 Python 计算或 AI 服务。

## 贡献本 Skill

用户要求贡献、提交、发布修改或创建 Pull Request 时，先读取 [CONTRIBUTING.md](CONTRIBUTING.md)。不要假定安装目录是 Git 仓库。需要修改课程页面时，遵循配套项目 `creator-skills/SKILL.md`，保留现有模块身份和素材 UUID。

## 完成标准

学习请求：解释选定知识点，并依据学习者的问题继续引导。演示请求：确认服务可访问、目标页面渲染及所需交互可用，再提供地址。缺失配套环境或更新来源时，明确说明当前能完成的部分。
