# 网页可视化与服务配套

runtime 只保存网页预览、后端服务、启停管理及服务运行数据。

- start.ps1 / stop.ps1：统一启动、查看状态与停止服务。
- frontend/：课程目录、路由、Guide 和 PPT 网页入口。
- backend/：Python 计算、AI 评价、任务与学习记录服务源码。
- services/：预览和后台服务的管理实现。
- data/：按需生成的日志、状态、缓存、数据集及构建结果。

公共组件、设计系统、内容生成工具、验证、测试和独立演示属于 ../creater-skills/。依赖安装属于 ../environment/；课程内容属于 ../courses/。

安装与启停见 [根目录说明](../README.md)，创作验证使用 `./creater-skills/check.ps1`（从项目根目录执行）。
