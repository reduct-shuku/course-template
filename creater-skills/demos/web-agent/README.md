# 独立 Web Agent 演示

React + LangChain.js 浏览器智能体演示，展示计算、时间、网页检索和待办工具的真实调用过程。支持配置模型后的真实运行，也保留不需要密钥的离线演示。与课程主站和 Python 后端独立。

从项目根目录执行：

```powershell
.\environment\install.ps1 -Kind agent-demo
.\runtime\start.ps1 -Kind agent-demo
.\runtime\start.ps1 -Kind agent-demo -Status
.\runtime\stop.ps1 -Kind agent-demo
.\creater-skills\check.ps1 -Kind agent-demo
```

默认访问 http://127.0.0.1:5183 。本目录属于创作工具集，保存演示源码与 HTML，依赖、锁文件、Vite 和 TypeScript 配置位于 environment/agent-demo/，构建结果位于 runtime/data/build/agent-demo/。

前台调试：`npm --prefix environment/agent-demo run dev`。演示中的供应商配置与课程后端 AI 配置各自独立；真实模型调用需对应接口和浏览器网络权限。

公开模板不包含 API 密钥。真实运行前，在设置面板填写自己的 API 地址、密钥和模型；也可选择无需密钥的离线演示。设置只保存在当前浏览器，不应将实际密钥写入源码或提交到仓库。
