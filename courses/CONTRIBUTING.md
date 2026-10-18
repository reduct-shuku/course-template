# 贡献互动课程库

本流程依据 Shuku 模板的贡献规则，适用于用户要求提交、发布或创建 Pull Request 时。

## 来源与范围

先读取同目录 shuku.json 的 repository、ref、path、version。当前 repository 尚未配置；必须由课程维护者提供实际仓库后才能检查更新或发起贡献。不得使用 Shuku 格式模板仓库作为本课程的来源。

不假定 Skill 安装目录是 Git 仓库。在独立临时目录获取目标仓库指定 ref，以当前安装版本为基准识别本课程的修改；排除其他课程、凭据、运行日志、缓存和构建产物。发现来源信息矛盾或远程冲突时，向用户说明并等待处理。

当前 Skill 根目录为 courses/modules/，各课程源码位于其子目录。视觉生成源码在 Visual-Generation-Guide/，素材在 courses/assets/dc633d9a-a68e-4114-a1cd-8421c59cb222/。涉及素材时同时核对；保持各课程 outlines.json.moduleIdentity 不变。正式发布前必须确定素材与 Shared、运行环境的分发方式，当前课程库不是独立可启动的网页工程。

## 提交前确认

课程公开能力、行为或内容发生变化时，同步检查 version 和 changes。执行 GitHub 写操作前，展示可用且已认证的账号，让用户明确选择。

在 Commit、Push 或创建 PR 之前，展示修改目的、文件范围、版本变化、账号、目标仓库、分支、Commit Message、PR 标题和正文、验证结果，并取得用户确认。普通本地编辑和验证不需要这一步。

## 验证

在 course-template 根目录执行：

```powershell
.\creater-skills\check.ps1 -Kind courses -Python C:\path\to\python.exe
.\creater-skills\check.ps1 -Kind frontend
```

格式校验需 Python 3.9+，且不要求安装后端依赖。还需确认 Markdown 相对链接有效、Guide 与 PPT 可访问，页面变更满足 1600×900 画布及交互检查。涉及身份时按配套身份指南验证签名。

在临时 Git 工作区核对 git diff --check、git status --short 和 git diff，确认最终变更只包含用户确认的课程范围。

## 发布贡献

得到确认后在用户选择的账号中准备 Fork、从最新 ref 创建工作分支、Commit、Push 并向目标仓库指定 ref 创建 PR。不强推默认分支、不绕过分支保护、不直接修改官方默认分支、不自动合并。登录、权限、冲突或分支保护阻塞时停止远程操作并说明原因。
