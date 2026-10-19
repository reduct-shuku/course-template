---
name: collaborate-course
description: 在个人 Fork 工作分支完善已有课程，生成预览并通过 Pull Request 提交共创。
---

1. 按术库“共创说明”克隆个人仓库，切换指定工作分支。保留所选基础版本的课程内容和来源信息，阅读 ../SKILL.md。
2. 内容修改放在 courses/；创作工具、公共组件和运行环境沿用现有框架。
3. 安装依赖：npm --prefix environment/frontend ci。本地运行 npm --prefix environment/frontend run dev 检查课程。
4. React/TSX 课程完成后执行 python3 creater-skills/tools/package_course.py，生成 courses/preview/；courses/shuku.json 保留 preview.entry。纯 static HTML 课程沿用其 entry，无需运行 React 构建。
5. 将课程源码、shuku.json 和生成的 preview 一起提交，推送到说明指定的个人工作分支。不要提交 course.zip、api_token 或 runtime/data。
6. 回到术库“我参与的共创”，进入工作区，点击“同步我的修改”，检查“预览我的修改”，再点击“提交共创建议”。已有 PR 的后续修改继续推送同一分支并同步。

共创通过个人 Fork 和 PR 交付，不使用课程所有者的上传凭证，不调用阶段版本上传接口。审核者查看当前 PR 提交对应的预览；有新提交后需重新审核。
