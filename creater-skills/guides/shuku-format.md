# Shuku 课程 Skill 格式

标准来源：[reduct-shuku/reduct-shuku-skill-template](https://github.com/reduct-shuku/reduct-shuku-skill-template)。官方校验脚本原样保存于 `creater-skills/tools/checks/validate_shuku_skill.py`，取自该仓库 main 的 scripts/validate_skill.py（2026-10-18）；升级规范时先比较上游要求再替换。

## 课程单元

本项目以 `courses/modules/` 为 Shuku Skill 包根目录，统一维护一套元数据和使用入口；`Visual-Generation-Guide/` 等子目录存放具体课程内容，不重复放置 Shuku 根元数据。包根目录必需：

- README.md：课程用途、使用方式和运行依赖。
- SKILL.md：YAML frontmatter 含 name、description；说明课程使用、版本检查、贡献入口和完成条件。
- shuku.json：Shuku 元数据，区别于页面大纲 outlines.json 和旧 Agent 集成 skill.manifest.json。
- CONTRIBUTING.md：读取来源、核对修改与冲突、版本更新、账号选择、提交前确认、验证和 PR 流程。

本模板的页面、组件和素材继续使用现有目录。上游允许自由组织课程内容，不要求把 courses、runtime 或 creater-skills 改成固定的嵌套布局。

## 元数据

shuku.json.schema_version 固定为 1；name 使用小写字母、数字和连字符，与 SKILL.md 的 name 一致；version 为三段数字语义版本。title 和 description 为实际课程信息。

repository 必须为课程实际所属的 `https://github.com/owner/repo`，不带 .git；未知时向用户索取，不能编造地址或使用格式模板的地址。ref 为实际分支或标签。path、entry 必须按官方校验器的组合规则指向实际存在的入口：校验器检查 `<校验根目录>/<path>/<entry>`，path 为 `.` 时直接检查 entry。调整到合集发布方式时，需要同时验证远程更新路径与此组合的可用性，不可机械填入本地绝对路径。

本项目目前使用 `build_profile: skill`、`entry: SKILL.md`、`path: .`，表示整个课程库 Skill 包；独立发布需准备真实课程库仓库与配套依赖。上游还支持 static，要求入口为真实存在的 .html；仅添加元数据不能把依赖 Shared 的 React 源码变成独立静态课程。

当前上游校验器要求 type 为 official，照其枚举填写仅表示满足该格式字段，不能据此宣称课程已获平台审核。包可包含多个课程，因此包元数据不使用某一个课程的 UUID 作为 course_id；各课程 outlines.json.moduleIdentity 继续独立维护，保持 UUID 与签名不变。

每次触发课程 Skill，按 repository、ref、path 检查远程 shuku.json；远程版本更高时展示 changes，经用户同意后更新；不能访问来源时说明并继续本地使用。贡献操作按课程 CONTRIBUTING.md 执行。

## 校验

在 course-template 根目录运行（Python 3.9+，仅标准库）：

```powershell
.\creater-skills\check.ps1 -Kind courses
# 或显式指定解释器
.\creater-skills\check.ps1 -Kind courses -Python C:\path\to\python.exe
# 直接校验包根目录
python .\creater-skills\tools\checks\validate_shuku_skill.py .\courses\modules
```

不为已有课程添加 `.template` 来绕过来源地址或占位符检查。repository 尚未提供时，保留明确未配置状态并报告严格校验失败，不能宣称发布就绪。

格式通过后，仍需按创作规范验证身份、Guide/PPT 及交互；该脚本不执行课程代码，也不证明课程可以脱离本项目独立运行。
