# 互动课程模板

项目按四类职责组织：创作工具集、服务运行配套、环境安装、课程内容。

```text
course-template/
├── README.md
├── AGENTS.md
├── creater-skills/          创作规范、组件、设计系统、工具、验证与演示
├── runtime/                 网页预览、后端服务、启停与运行数据
├── environment/             安装入口、依赖清单、构建配置和本地环境
└── courses/                 课程源码、大纲、讲稿和素材
```

## 安装与预览

安装 Node.js 后，在项目根目录执行：

```powershell
.\environment\install.ps1
.\runtime\start.ps1
```

打开 http://127.0.0.1:5173 。默认只启动课程网页，不要求 Python、Cloud 仓库、数据库或模型密钥。

- `/`：课程目录。未创建课程时显示空态。
- `/shared/ui-kit`：公共组件和设计系统预览。
- `/scenedeck/`：PPT 播放器。

当前已导入 **视觉生成：从噪声到图像**（20 个实际呈现页）：

- Guide：`/modules/visual-generation-guide`
- PPT：`/scenedeck/?deck=visual-generation-guide`
- 源码与适配说明：[Visual-Generation-Guide](courses/modules/Visual-Generation-Guide/README.md)

```powershell
.\runtime\start.ps1 -Status
.\runtime\stop.ps1                 # 停止本模板启动的服务
.\creater-skills\check.ps1                # 类型检查和生产构建
```

预览进程在后台启动，不打开额外窗口。重新启动时复用已运行的服务；停止只针对本模板记录且通过实例校验的进程。修改 .env.local 后需要停止并重新启动。命令都可从其他工作目录以完整路径调用。

前台调试和原生 npm 命令：

```powershell
npm --prefix environment/frontend run dev
npm --prefix environment/frontend run typecheck
npm --prefix environment/frontend run build
npm --prefix environment/frontend run preview
```

根目录不再放 package.json；不能直接在根目录执行 npm run dev。

## 创建课程

1. 阅读 [创作规范](creater-skills/SKILL.md) 和 [课程目录说明](courses/README.md)。
2. 使用 UI Kit 检查组件，通过 `@shared/react` 导入公共组件。
3. 在 `courses/modules/<课程名>/` 创建 outlines.json、React 页面、Guide 入口和 PPT 适配器。首页会自动发现。
   Shuku 标准的 README.md、SKILL.md、shuku.json、CONTRIBUTING.md 统一位于 `courses/modules/`；新增课程时同步更新课程库入口，详见 [Shuku 格式指南](creater-skills/guides/shuku-format.md)。
4. 新课程创建前按 [身份指南](creater-skills/guides/module-identity.md) 初始化独立密钥，创建后签发并验证身份。
5. 素材放在 `courses/assets/<签名 UUID>/`，统一通过 moduleAssetUrl 引用。
6. 运行 `./creater-skills/check.ps1 -Kind courses` 校验 `courses/modules/` 的 Shuku 格式（Python 3.9+，无后端依赖）。需填写课程库实际所属的 GitHub 仓库；当前 repository 待配置，严格校验会明确报错。

课程画布固定为 1600×900；Guide 和 PPT 共享页面。课程 URL 保持 `/modules/<目录名小写>`，URL 与磁盘路径不同。

## 上传到术库

将上传凭证保存为仓库根目录的 `api_token` 文件，完成阶段版本后按 [术库上传方法](UPLOAD.md) 打包、上传并查询结果。

## 可选后端与 AI

需要 Python 3.10+。默认安装使用 PATH 中的 Python，可通过 -Python 指定：

```powershell
.\environment\install.ps1 -Kind backend -Python C:\path\to\python.exe
.\runtime\start.ps1 -Kind records
.\runtime\start.ps1 -Kind vision
```

安装器创建 `environment/backend/.venv/`，后端脚本优先使用它。记录服务端口 59411，视觉服务端口 28431。默认不预热模型；实际训练或识别需另外安装匹配 CPU/CUDA 的 torch、torchvision 并准备数据和权重。设置 IDL_PREWARM_INFERENCE=1 可启用预热。

配置 AI 供应商后启动代理与评价服务（Anthropic Messages 兼容协议）：

```powershell
$env:LLM_BASE_URL='https://your-provider.example'
$env:LLM_API_KEY='your-key'
$env:LLM_MODEL='your-model'
.\runtime\start.ps1 -Kind proxy
.\runtime\start.ps1 -Kind assessment
```

模型代理端口 59413，评价端口 28432。Shared Question 发送内联题目和参考答案，不依赖原课程题库。密钥只保存在后端环境变量或 `environment/backend/settings.json`，不得写入课程或 VITE_* 变量。

`-Kind backend` 启动四个后端服务；`-Kind all` 启动课程前端和四个后端，需要完整依赖与 AI 配置。单服务支持 -Port，后端支持 -Python；vision 支持 -Device 和 -Course。

```powershell
.\runtime\start.ps1 -Kind records -Status
.\runtime\stop.ps1 -Kind records
.\creater-skills\check.ps1 -Kind backend
```

学习记录默认不启用。需要时启动 records，在 `environment/frontend/.env.local` 设置 VITE_ENABLE_TELEMETRY=true 并重启预览。

可选 Cloud 集成需准备外部 Cloud 仓库、数据库及其依赖，设置 IDL_CLOUD_REPOSITORY，并以 -Kind api 启动。在 `environment/frontend/.env.local` 设置 VITE_USE_CLOUD_RUNTIME=true 后重启前端。模板不内置 Cloud API 源码。

## 独立 Web Agent 演示

```powershell
.\environment\install.ps1 -Kind agent-demo
.\runtime\start.ps1 -Kind agent-demo
.\runtime\stop.ps1 -Kind agent-demo
.\creater-skills\check.ps1 -Kind agent-demo
```

地址 http://127.0.0.1:5183 。源码位于 creater-skills/demos/web-agent/，依赖与配置位于 environment/agent-demo/；详见 [演示说明](creater-skills/demos/web-agent/README.md)。

## 数据、构建与生成工具

| 位置 | 用途 |
|---|---|
| environment/frontend/node_modules/ | 课程前端依赖 |
| environment/agent-demo/node_modules/ | 独立演示依赖 |
| environment/backend/.venv/ | Python 环境 |
| environment/backend/.private/ | 本模板签发私钥，禁止分发或提交 |
| courses/identity-public-key.txt | 签发公钥，初始化后随课程保存 |
| runtime/data/logs/ | 服务日志 |
| runtime/data/services/ | 预览进程实例与停止凭据，不分发 |
| runtime/data/history/ | 本地学习记录 |
| runtime/data/datasets/ | 数据集、模型和训练产物 |
| runtime/data/build/ | 前端及演示的构建结果 |
| runtime/data/cache/ | Vite 缓存 |

这些运行目录按需生成，不作为初始课程内容。重新分发模板时排除 node_modules、.venv、.private 和 runtime/data；不要删除课程签发公钥。

[内容生成与验证工具](creater-skills/tools/README.md) 包含缩略图、页面边界、候选答案和 t-SNE / Grad-CAM 工具。安装后端环境后先激活它：

```powershell
.\environment\backend\.venv\Scripts\Activate.ps1
python -m idl_authoring.content.generate_scenedeck_thumbnails --module your-module
.\creater-skills\check.ps1 -Kind all
```

当前包含已导入的视觉生成课程及其教学素材，不包含真实训练集、模型权重或供应商密钥。该课程的教学模拟在浏览器执行，预览无需启动 Python 计算或 AI 服务。

## 整理后验证

已通过 creater-skills/check.ps1 的两套前端构建、28 项测试和身份验证。浏览器验证了空课程预览、公共组件、临时课程自动注册、Guide/PPT 交互、素材加载与新 idl_authoring 工具包的缩略图生成；两套网页预览和记录服务的启停已检查。临时课程和验证产物不包含在交付模板中。

未调用真实上游 AI，也未执行需要外部训练集或权重的模型训练；可选 Cloud 链路未在此次验证中启动。

已导入课程的验证详情见 [Visual-Generation-Guide 说明](courses/modules/Visual-Generation-Guide/README.md#预览核对)：20 页渲染和画布边界、开场照片、GAN/Diffusion 代表性交互、素材与目录缩略图均已检查。
