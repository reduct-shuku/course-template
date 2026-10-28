# 课程大纲与注册

大纲讨论和文件规范见 [课程大纲](../references/design/course-outline.md)。每页仅保存 title 和 snippet，播放器场景 ID、交互和制作状态保存在实现代码中。

课程实现位于 courses/modules/<Module>/，按实际进度添加 Guide/PPT 入口；runtime/frontend/src/app/modules.tsx 自动发现模块。path 使用 /modules/<目录名小写>，entry 与 ppt.entry 必须对应实际存在的文件。独立页面文件放 pages/<语义页目录>/，开始当前页时才创建。

身份按 [签名指南](module-identity.md) 处理。课程库的 README.md、SKILL.md、shuku.json、CONTRIBUTING.md 统一位于 courses/modules/，按 [Shuku 格式](shuku-format.md) 维护；courses/shuku.json 是平台上传清单，不能互相覆盖。
