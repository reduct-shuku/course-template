# 模板工具索引

本模板的工具与来源仓库不同。以下路径和命令均从模板根目录执行，只调用当前可用工具，不使用来源仓库的 scripts/tools.py 或 backend/ 路径。

| 任务 | 命令 |
|---|---|
| 初始化大纲（不会覆盖现有文件） | python creator-skills/tools/init_outline.py --directory MyCourse --title "课程标题" |
| 身份密钥首次初始化 | 激活 environment/backend/.venv 后执行 python -m idl_authoring.keys；已有课程或密钥时不重建 |
| 签发 / 检查身份 | python -m idl_authoring.identity；检查时加 --check |
| 前端类型检查 | npm --prefix environment/frontend run typecheck |
| 生产构建 | npm --prefix environment/frontend run build |
| 生成正式缩略图 | 激活 Python 环境后执行 python -m idl_authoring.content.generate_scenedeck_thumbnails --module MyCourse |
| 页面边界检查 | 设置 PPT_DEBUG_PORT、PPT_LESSON_URL、PPT_SLIDE_IDS 后执行 npm --prefix environment/frontend run check:bounds |
| 模板后端与工具回归 | creator-skills/check.ps1 -Kind backend |
| 技能文档、路径与初始化工具回归 | python -m pytest creator-skills/tests/test_creator_skill.py -q |
| 构建上传课程包 | python creator-skills/tools/package_course.py，见 [UPLOAD.md](../../UPLOAD.md) 和 [上传 Skill](../upload/SKILL.md) |

初始化工具仅创建 courses/modules/<Module>/outlines.json，已有文件不读写。缺少签名身份时随后按身份指南签发；不在初始化时预建逐页目录或 React 占位文件。大纲阶段每页只写 title 与 snippet，播放器 ID 在实现代码中维护。

模板预览使用 runtime/start.ps1，停止使用 runtime/stop.ps1。Python 工具路径、额外依赖、模型与素材处理见 [现有工具](../tools/README.md)。环境和服务都沿用模板布局，不额外复制来源仓库的运行系统。

逐页设计、prompt、截图与检查记录写入 courses/modules/<Module>/pages/<Page>/_scratchpad/；整份原稿与汇总记录放模块级 _scratchpad/。检查截图必须真实打开；生成正式缩略图不能替代关键交互、画布与文字溢出的验收。来源中的 capture.slides、check.course、analyze.pages 等统一命令尚未移植到本模板，不假称已有这些命令或其统计结果。
