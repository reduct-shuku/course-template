# 课程模板工作规则

- 创作规范入口为 [creater-skills/SKILL.md](creater-skills/SKILL.md)，按需读取 guides/。
- 四个主目录固定为 creater-skills/、runtime/、environment/、courses/。
- 课程实现仅在 courses/modules/，课程素材在 courses/assets/<签名 UUID>/。
- courses/modules/ 是 Shuku 包根目录，统一保存 README.md、SKILL.md、shuku.json、CONTRIBUTING.md；课程实现放其子目录。细则见 creater-skills/guides/shuku-format.md，使用 check.ps1 -Kind courses 校验。实际 GitHub 来源未知时须明确待配置，不得编造。
- 公共组件与设计系统在 creater-skills/shared/，通过 @shared/react 导入；Shared 不得依赖具体课程。
- 课程磁盘路径与 /modules/<目录名小写> URL 分开处理；身份签名不得因移动基础设施而重签。
- 课程页固定 1600×900，复用 ContentBlock、Typography、MathFormulaBlock 和 SceneDeck。
- Grid/Flex 子项必须可收缩；完成后验证画布边界、1600×900 截图、默认及交互状态。
- 安装使用 environment/install.ps1；启停使用 runtime/start.ps1、runtime/stop.ps1；验证使用 creater-skills/check.ps1。
- 配置集中到 environment/，日志/缓存/构建/数据集中到 runtime/data/；密钥不得写入前端或课程。
- 不查看 Git 历史，除非用户明确要求。不要覆盖用户已有课程或设计偏好。

- creater-skills 集中创作规范、公共组件、设计系统、生成工具、验证和演示；runtime 仅保留预览和后端服务配套，不放创作工具。
