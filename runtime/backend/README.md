# 后端服务源码

代码位于 src/idl_backend/；包配置和依赖在 ../../environment/backend/；测试在 ../../creater-skills/tests/。

保留 contracts（身份与任务）、datasets（数据加载）、vision（特征、训练、推理）、assessment（结构化评价）、providers（模型配置）、jobs（任务执行）、local（服务管理与可选 Cloud）；离线创作工具已迁至 creater-skills/tools/python/idl_authoring/。

安装：根目录执行 `./environment/install.ps1 -Kind backend -Python <Python3.10+路径>`。
启动：`./runtime/start.ps1 -Kind records|vision|proxy|assessment`（每次选择一个）；验证：`./creater-skills/check.ps1 -Kind backend`。

默认数据根为 runtime/data/datasets/，可用 IDL_DATA_DIR / IDL_MODEL_DIR / IDL_ARTIFACT_DIR 覆盖；课程登记从 courses/modules/ 读取。后台进程由模板根路径定位，调用脚本不依赖当前工作目录。

没有内置模型权重、训练集或供应商密钥；实际计算与 AI 调用需另外配置。完整端口、AI 与可选 Cloud 说明见 ../../README.md。
