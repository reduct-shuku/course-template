# 模块身份与资源

本模板保留 UUID v4 与 Ed25519 签名，不替换为仅有 UUID 的身份。

- 创建或检查身份：[课程身份与签名](../../guides/module-identity.md)。
- 课程正式资源、缩略图与引用：[模块资源](../../guides/module-assets.md)。
- 图文上传及审核：[上传课程](../../upload/SKILL.md)，个人 Fork 共创：[共创编辑](../../collaboration/SKILL.md)。

逐页设计图、prompt 和检查截图放 courses/modules/<Module>/pages/<Page>/_scratchpad/；课程整体原稿、大纲备份和汇总记录放模块级 _scratchpad/。正式资源移入 courses/assets/<UUID>/ 后再通过 @shared/react 的 moduleAssetUrl 引用，运行时不得依赖 _scratchpad/。
