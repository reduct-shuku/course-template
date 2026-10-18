# 上传课程到术库

课程初始化后，将上传凭证原样保存到仓库根目录的 `api_token` 文件，文件中只放 Token。上传服务地址使用课程创作说明中的“术库地址”，默认是 `https://shukuproduct.reduct.cn`。

## 准备课程包

完成课程后导出单门课程的静态页面，将页面、所需资源和上传描述 `shuku.json` 打包为 `course.zip`。ZIP 根目录必须有 HTML 入口（默认 `index.html`）和 `shuku.json`，资源使用相对路径。不要直接压缩整个开发仓库；`api_token` 留在本地，不加入 ZIP。

ZIP 和解压后的总大小分别不超过 100 MiB，最多 100 个文件；`shuku.json` 不超过 32 KiB。上传描述使用创作说明给出的课程信息，后续阶段保留同一 `courseKey`，更新 `stageNote`。模板 `courses/modules/shuku.json` 是课程库元数据，与上传描述分别维护。

首次上传与更新阶段版本使用同一个接口。每次上传是完整课程快照，未包含的旧课程文件会被删除。

## 上传

在含 `api_token` 和 `course.zip` 的仓库根目录运行以下示例，需要 curl 和 Python 3。使用其他术库环境时，先设置 `SHUKU_URL` 为课程创作说明中的术库地址。

```bash
SHUKU_URL="${SHUKU_URL:-https://shukuproduct.reduct.cn}"
TOKEN="$(tr -d '\r\n' < api_token)"
UPLOAD_ID="${UPLOAD_ID:-$(python3 -c 'import uuid; print(uuid.uuid4())')}"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $TOKEN" \
  -H "Idempotency-Key: $UPLOAD_ID" \
  -F "file=@course.zip;type=application/zip" \
  "$SHUKU_URL/api/agent/courses/upload"
```

成功接收返回 HTTP 202 和 `taskId`，此时尚未完成 GitHub 同步。每个新阶段使用新 `UPLOAD_ID`；网络重试时复用该 ID 和相同 ZIP 字节。

## 查询结果

将返回的 `taskId` 设为 `TASK_ID`，使用同一凭证查询：

```bash
SHUKU_URL="${SHUKU_URL:-https://shukuproduct.reduct.cn}"
TOKEN="$(tr -d '\r\n' < api_token)"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $TOKEN" \
  "$SHUKU_URL/api/agent/tasks/$TASK_ID"
```

每隔 3–5 秒查询一次：`queued`、`syncing`、`retry_wait` 表示处理中；`succeeded` 表示上传和私有 GitHub 仓库同步完成，向用户返回课程信息和预览链接（术库地址加 `result.previewUrl`）；`failed` 时读取 `error.code`、`error.message` 和 `error.retryable`。401/403 表示凭证不可用，429 按 `Retry-After` 等待。等待超过 5 分钟时保留任务编号并报告当前状态。

首次上传创建私有课程，后续上传更新同一课程。用户可在术库提交公开审核。凭证默认长期有效，用户可在个人信息中撤销。
