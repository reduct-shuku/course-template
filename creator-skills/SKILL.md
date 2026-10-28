---
name: creator-skills
description: 在当前仓库中规划、设计、实现、修改和评估 React PPT 演示。包括仅在聊天中讨论汇报主线、设计或修改大纲，以及从主题或材料创作演示、将既有 PPT/PDF/截图改编为 React 演示、继续开发或修复已有模块。支持教学、科研和商业汇报；不用于普通网站开发或一般文档编辑。
---

# React PPT 创作

## 模板准备与术库边界

本模板使用 creator-skills/、environment/、runtime/、courses/ 四个主目录。公共组件由 @shared/react 导入，课程实现位于 courses/modules/，素材位于 courses/assets/<UUID>/。

首次仅收到术库创作或共创说明时，只准备本地项目、读取必要规范并保存给定信息及根目录 api_token，等待用户具体创作要求；不因说明中已有标题或简介就制作、构建、上传或提交。用户已经明确给出制作要求时按已有授权推进。

安装、预览、停止和验证分别使用 environment/install.ps1、runtime/start.ps1、runtime/stop.ps1、creator-skills/check.ps1。命令和布局见 [模板工具索引](references/tools.md)。本模板保留 Ed25519 签名身份；不复制来源仓库的身份密钥、计算服务或部署配置。

## 开始任务

1. 确定目标模块、用户要求和已有成果。
2. 必须读取[流程共用说明](references/workflow/common.md)，再判断任务模式，读取对应 Workflow。
3. 确定当前阶段，从该阶段继续；复用已有大纲、设计、代码和确认结果。
4. 按当前动作读取必要资料，不预读整个参考目录。

涉及汇报主线、章节、开场、内容取舍或大纲时，执行[大纲](references/design/course-outline.md)规范；仅在聊天中讨论、尚不修改文件，也属于该动作。已读过且仍在上下文中的资料无需反复读取，但每轮须按用户最新要求判断当前交付是主线讨论、章节结构还是逐页题目与演讲稿，不能用“已读取”代替执行。

| 任务模式 | 适用情况 | Workflow |
|---|---|---|
| 从零创作 | 从主题、文字、论文或其他材料组织演示 | [从零创作](references/workflow/from-scratch.md) |
| 参考改编 | 以既有 PPT、PDF 或逐页截图作为创作依据 | [参考改编](references/workflow/reference-adaptation.md) |

任务只分为上述两种模式。继续制作、修改或修复已有模块时，沿用原 Workflow 的制作与确认流程，从当前阶段接续，不因模块或 React 文件已经存在而切换模式。

## 执行原则

- 每页明确主要信息或核心问题，内容与整份演示的目标一致。
- 图形、图片、动画和交互应承担表达或解释功能。
- 生成视觉设计图前，必须读取[页面设计指导](references/design/design.md)，实际打开相关成对视觉正反例，并将借鉴与避让的具体设计决策写入生图提示词；不能仅写“参考样例”或凭印象指定风格。
- 根据用户要求和当前 Workflow 决定大纲确认、设计预览及制作批次。
- 沿用已有确认与授权；局部修改只处理受影响内容及必要依赖。
- 仅在缺失信息会实质改变方向且无法合理推断时询问用户。
- 教学方法、习题、Guide 和讲稿按任务需要采用，不作为所有演示的必备内容。
- 页面制作与修改后执行基础检查；仅在用户明确要求打分、评分或执行 Rubric 时加载评分说明。“检查”“看看问题”“优化”不自动触发评分，评分不替代基础检查或用户验收。

完整执行与确认规则见[流程共用说明](references/workflow/common.md)。

## 工程约束

- 使用 React，沿用当前仓库的技术栈和模块入口，默认复用 creator-skills/shared 下的工程脚手架。
- 页面使用 1600×900 固定画布，由外层等比例缩放。
- 第一页不使用 `ContentBlock`，单独设计封面。其余页面默认使用 Shared `ContentBlock` 及其标准标题区，设计示意图阶段就遵守；只有用户明确要求其他版式时，才在指定范围内更换。视觉样例默认指导标题区以下的内容构图。
- 独立文字使用 Shared `Typography` 或已封装它的组件。
- 模块大纲位于 `courses/modules/<模块目录名>/outlines.json`。
- 大纲每页只写 `title`（题目）和 `snippet`（演讲稿），不增加其他页面字段。用户尚未提供的内容不自行补全。结构要求见[大纲](references/design/course-outline.md)。
- 每页独占 `courses/modules/<模块目录名>/pages/<语义页目录>/`，页面组件与同名样式放在该目录，不平铺在 `pages/` 下。该页的设计图、prompt、检查截图及临时脚本放在页目录内的 `_scratchpad/`；课程整体的原稿、大纲备份和汇总记录放在模块级 `_scratchpad/`。两级临时目录均由 Git 忽略，正式资源按工程约定保存。
- 页目录与 `_scratchpad/` 按实际制作需要创建，不根据大纲预建未开始页面的空目录或占位文件。
- 遵守模块身份、静态资源和公共组件边界。

## 按动作读取

执行相应动作前，读取对应资料。

| 动作 | 资料 |
|---|---|
| 讨论主线、章节与开场，或生成、修改大纲（含纯聊天） | [大纲](references/design/course-outline.md) |
| 设计或调整页面内容、构图与交互 | [页面设计指导](references/design/design.md) |
| 分析原稿及转换范围 | [参考与转换](references/workflow/reference-adaptation.md) |
| 编写或修改 React 页面 | [工程实现](references/engineering/implementation.md) |
| 创建或调整模块身份、资源 | [模块身份与资源](references/engineering/module-assets.md) |
| 检查实现并交付 | [基础检查与验收](references/eval/checks.md) |

## 按问题选读

仅加载与当前问题有关的资料。

| 问题 | 资料 |
|---|---|
| 习题与答案反馈 | [习题设计](references/design/quiz.md) |
| 用户明确要求页面质量评分 | [Rubric Evaluation](references/eval/rubric-evaluation.md) |
| 准备执行创作工具命令（含大纲初始化），或查询工具、依赖与命令 | [工具索引](references/tools.md)，执行前必读 |
| 大模型调用 | [大模型调用](references/computing/llm.md) |
| 模型与较重计算 | [模型计算](references/computing/gpu.md) |
| 用户明确要求采用个人偏好 | [个人偏好](references/preferences.md) |

## 完成与交付

- 按改动范围检查内容、实际渲染和相关交互。
- 实现后的视觉检查使用真实页面，设计示意图不能替代运行结果。
- 修复已发现的重大内容、布局和交互问题，并复验。
- 简要说明完成内容、实际验证结果及尚未解决的限制。
- 未执行或受阻的检查如实标记，不声称通过。


## 术库上传与共创

- 用户要求上传阶段版本时读取 [上传课程 Skill](upload/SKILL.md) 和 [上传说明](../UPLOAD.md)，从根目录 api_token 读取凭证，仅打包 courses/。保留给定 courseKey，凭证不进入课程包。
- 个人 GitHub Fork 的共创按 [共创编辑 Skill](collaboration/SKILL.md) 预览并提交 PR；未绑定 GitHub 的私有工作区沿用上传通路。
- 元数据、签名与课程库入口按 [Shuku 格式](guides/shuku-format.md)、[身份指南](guides/module-identity.md)、[课程注册](guides/course-outline.md) 维护；courses/modules/shuku.json 与 courses/shuku.json 不能互相替代。
- 修改本 Skill 后核对 [回归场景](evals/scenarios.json)，文档或规则维护本身不触发课程创作。
