# 上传课程到术库

课程初始化后，将上传凭证原样保存到仓库根目录的 `api_token` 文件，文件中只放 Token。上传服务地址使用课程创作说明中的“术库地址”，默认是 `https://shukuproduct.reduct.cn`。

## 准备课程包

上传对象是仓库中的 **`courses/` 内容创作文件夹**。将 `courses/` 里面的内容压缩为 `course.zip`，保留 `modules/`、`assets/` 等内部目录结构。压缩包根目录对应 `courses/`，不是整个模板仓库，也不是只上传某个构建输出目录。仓库根目录的 `api_token` 不在压缩范围内。

在模板仓库根目录先执行 `npm --prefix environment/frontend ci`，再执行 `python3 creater-skills/tools/package_course.py`。工具会在本地构建课堂到 `courses/preview/`，更新 `shuku.json` 的 `preview: {"entry":"preview/index.html"}`，并压缩完整 `courses/` 为 `course.zip`。上传操作也可直接交给 [上传课程 Skill](creater-skills/upload/SKILL.md)。

只保存未完成源码、不需要在线预览时，可以使用 `--source-only`，或运行以下打包示例：

```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

courses = Path("courses")
if not courses.is_dir():
    raise SystemExit("请在模板仓库根目录运行，确保 courses 文件夹存在。")
with ZipFile("course.zip", "w", compression=ZIP_DEFLATED) as package:
    for file in sorted(courses.rglob("*")):
        if file.is_file():
            package.write(file, file.relative_to(courses).as_posix())
```

例如 `courses/modules/课程名/` 会保存为 ZIP 内的 `modules/课程名/`，`courses/assets/` 保存为 `assets/`，`courses/shuku.json` 位于 ZIP 根目录。

ZIP 和解压后的总大小分别不超过 100 MiB，最多 1000 个文件、3000 个文件与目录项；`shuku.json` 不超过 32 KiB。后续阶段保留同一 `courseKey`，更新 `stageNote`。

接口以 ZIP 根目录的 `shuku.json` 校验课程信息，不要求 HTML 入口，也不限制 React/TSX 等课程源码扩展名。`schema_version` 为 1，包含 `courseKey`、`title`、`description`、`category`、`repositoryName`（首次必填）和 `stageNote`；`build_profile` 支持 `skill` 或 `static`。用创作说明的信息初始化 `courses/shuku.json`，保留原课程的版本、入口及其他规范字段；源码课程可以保留 `entry: "SKILL.md"` 和 `build_profile: "skill"`。

服务器保存完整课程并同步至私有 GitHub 仓库，不构建或执行源码。含有效 `preview.entry` 的包返回 `sourceOnly: false` 和本人可访问的 `previewUrl`；课堂只提供 preview 目录中的静态资源。没有预览时仍可保存源码，返回 `sourceOnly: true`、`previewUrl: null`。

用户登录术库后，在“课程共创 → 我要创建课程 → 我提交的课程”点击“预览课程”；确认后点击“发布我的课程”提交审核。审核通过后课程公开，退回则保持私有，修改后重新上传。

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
