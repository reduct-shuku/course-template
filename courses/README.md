# 课程创作内容

本目录只放课程和素材。当前已从原仓库复制 Visual-Generation-Guide，提供视觉生成课程的 Guide 和 PPT 预览；可按同样结构添加更多课程。

```text
courses/
├── modules/                Shuku 包根目录
│   ├── README.md           课程库使用说明
│   ├── SKILL.md            Shuku Agent 使用入口
│   ├── shuku.json          课程库元数据、版本与更新来源
│   ├── CONTRIBUTING.md     课程库贡献与发布流程
│   └── <CourseName>/       具体课程实现
│       ├── outlines.json   大纲、页面顺序、入口和签名身份
│       ├── GuidePage.tsx   Guide 入口，导出同名组件
│       ├── coursePpt.tsx   PPT 适配器，导出 deck
│       ├── pages/          页面 TSX 和 CSS
│       ├── data/           课程数据（可选）
│       └── services/       服务调用（可选）
└── assets/<签名UUID>/       图片、视频、模型和缩略图
```

初始化身份后还会生成 courses/identity-public-key.txt。私钥位于 environment/backend/.private/。

modules/ 是 Shuku 包根目录，课程子目录沿用页面和素材布局。标准、元数据填写与分发限制见 [Shuku 格式指南](../creator-skills/guides/shuku-format.md)。运行 `./creator-skills/check.ps1 -Kind courses` 校验课程库；需要 Python 3.9+，无需后端依赖。

modules/ 已补齐基础文件，repository 尚待提供实际 GitHub 仓库；该项未填写前严格校验会失败。当前采用 skill 模式，通过完整 course-template 提供网页预览，不能将模块目录直接当作独立静态 HTML 包。

outlines.json 示例结构：

```json
{
  "id": "your-course",
  "title": "课程标题",
  "path": "/modules/coursename",
  "entry": "GuidePage.tsx",
  "ppt": { "entry": "coursePpt.tsx", "path": "/scenedeck/" },
  "pages": []
}
```

path 是 URL，必须为 /modules/ 加课程目录名的小写形式。entry 文件需导出同名组件。PPT 文件导出满足 `@shared/react/presentation` 的 DeckDefinition；每页提供 SceneDefinition，顺序与 outlines 一致。

公共能力通过 `@shared/react` 导入，避免手算跨目录相对路径。页面、讲稿、数据、状态与专属 CSS 留在当前课程。素材通过 moduleAssetUrl 引用。

安装与预览使用根目录说明中的 environment/install.ps1 和 runtime/start.ps1。完整规范见 [creator-skills/SKILL.md](../creator-skills/SKILL.md)。
