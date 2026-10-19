---
name: upload-course
description: 完成本地课程阶段后，将 courses 源码和在线预览一起上传到术库。
---

1. 读取课程创作说明，将课程信息写入 courses/shuku.json；后续保留 courseKey，更新 stageNote。上传凭证读取仓库根目录 api_token。
2. 安装前端依赖：npm --prefix environment/frontend ci。
3. 在仓库根目录执行 python3 creater-skills/tools/package_course.py。本地构建并写入 courses/preview，再将完整 courses 压缩为 course.zip。不要只上传 preview。
4. 按 ../../UPLOAD.md 的上传和查询示例发送 ZIP，等待任务 succeeded，向用户返回预览链接。
5. 用户登录术库，在“课程共创 → 我要创建课程 → 我提交的课程”预览并点击“发布我的课程”。管理员审核通过后公开；Agent 上传本身只保存私有草稿。

构建失败先修复再上传。只需备份未完成源码时使用 --source-only；没有预览的阶段不能提交公开审核。

已有公开课程的 Fork 共创请使用 ../collaboration/SKILL.md，不使用此阶段上传流程。
