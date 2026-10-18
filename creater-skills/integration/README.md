# 可选自动化接入

skill.manifest.json 是本项目的运行描述清单，供理解该格式的外部工具使用，不是 npm 或 Vite 必需文件。

本清单的 runtime.workingDirectory 相对于清单所在目录解析为 ../..（项目根目录）。生命周期命令随后从项目根目录执行。初始化使用 environment/install.ps1，启动使用 runtime/start.ps1，验证使用 creater-skills/check.ps1，停止使用 runtime/stop.ps1。

接入工具若使用不同的 workingDirectory 约定，应显式把工作目录设为模板根目录。仅手工制作和预览时无需读取本清单。创作 Skill 的入口为 ../SKILL.md。
