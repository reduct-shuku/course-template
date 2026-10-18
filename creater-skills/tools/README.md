# 开发辅助、生成与验证

从项目根目录执行下列命令。Python 工具先安装并激活 environment/backend/.venv。

Python 创作工具源码统一位于 tools/python/idl_authoring/；身份工具使用 `python -m idl_authoring.keys` 初始化独立密钥，使用 `python -m idl_authoring.identity` 签发和验证。服务包 idl_backend 只负责计算、评价与身份读取等运行配套。

| 工具 | 用途与运行方式 |
|---|---|
| checks/validate_ppt_bounds.mjs | `npm --prefix environment/frontend run check:bounds` |
| content/generate_decision_candidate_cache.mjs | `npm --prefix environment/frontend run cache:decision` |
| content/generate_digit_tsne_records.py | `python creater-skills/tools/content/generate_digit_tsne_records.py --help` |
| Python 缩略图 | `python -m idl_authoring.content.generate_scenedeck_thumbnails --module your-module` |
| Python 媒体工具 | `python -m idl_authoring.media.remove_green_screen input.mp4` |
| Python 模型工具 | `python -m idl_authoring.models.train_emnist_mobilenet_v3 --help` |

缩略图工具使用 environment/frontend/ 的 Vite 依赖和配置，输出 courses/assets/<签名UUID>/scenedeck-thumbnails/。需要 Edge、Chrome 或 Playwright Chromium；不依赖外部 Cloud。

画布边界检查需要开启调试端口的浏览器，设置 PPT_DEBUG_PORT（默认 9223）、PPT_LESSON_URL（完整页面 URL）和 PPT_SLIDE_IDS（逗号分隔）。

候选答案生成需设置 IDL_CANDIDATES_FILE（包含 rows 数组的 JSON），供应商配置来自 environment/backend/settings.json；结果默认在 runtime/data/cache/assessment/，可通过 LANGCHAIN_PRECOMPUTED_CACHE_DIR 覆盖，与后端读取路径保持一致。Grad-CAM 和 t-SNE 工具需设置 IDL_COURSE_UUID 为已签发课程身份，并准备对应训练数据、图像和额外模型依赖。脚本不是预置课程内容。

自动检查入口：`./creater-skills/check.ps1 -Kind frontend|backend|agent-demo|all`，实际执行时选择一个 Kind 值。
