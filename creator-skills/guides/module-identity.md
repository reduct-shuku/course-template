# 课程身份与签名

先在项目根目录执行 `./environment/install.ps1 -Kind backend`，然后激活 Python 环境：

```powershell
.\environment\backend\.venv\Scripts\Activate.ps1
# 首次创建任何课程前，只执行一次：
python -m idl_authoring.keys
# 创建 courses/modules/<课程名>/outlines.json 后：
python -m idl_authoring.identity
python -m idl_authoring.identity --check
```

初始化生成 `courses/identity-public-key.txt` 和 `environment/backend/.private/module-identity-ed25519.pem`。已有密钥或课程时禁止重新初始化。公钥随课程保存；私钥保密备份，禁止提交、分发或复制原仓库私钥。

签发工具扫描 courses/modules/*/outlines.json，仅为缺少 moduleIdentity 的模块签发 UUID v4 和 Ed25519 签名。已有身份保持不变；任何身份无效都会停止，不自动修复或重签。

签名覆盖课程 URL path（/modules/<目录名小写>）与 UUID，不覆盖标题或页面内容。迁移基础设施不改变 URL 或身份。验证使用本模板初始化的公钥；不要修改已签发课程对应的公钥或私钥。
