# google-user-auth

OpenClaw 的个人 Google OAuth Skill：完成首次授权、保存用户 refresh token，并为 Gmail、Google Analytics、Search Console、Site Verification 和 Indexing API 换取短期 access token。

## 包含内容

- `scripts/authorize_google_user.py`：首次授权或 scope 变化时运行，打开 Google 授权页并接收本地回调。
- `scripts/exchange_code.py`：由授权脚本自动调用，将一次性授权码交换为 refresh token。
- `scripts/get-token.sh`：读取用户 token JSON，输出短期 access token。
- `SKILL.md`：Skill 调用顺序与安全边界。

## 安装后需要准备的本机文件

将 Google Cloud 下载的桌面 OAuth Client JSON 保存为：

```text
/root/.openclaw/skills/google-user-auth/google-oauth-client.json
```

首次授权完成后，Skill 自动生成：

```text
/root/.openclaw/skills/google-user-auth/google-user-token.json
```

这两个文件以及 `.env` 都被 `.gitignore` 排除，不能提交到仓库。

## 首次授权

```bash
python3 /root/.openclaw/skills/google-user-auth/scripts/authorize_google_user.py
```

默认申请 Gmail、Analytics、Search Console、Site Verification 和 Indexing 的授权范围。需要不同范围时传入 `--scopes "..."`。

## 日常换取 access token

```bash
/root/.openclaw/skills/google-user-auth/scripts/get-token.sh \
  "https://www.googleapis.com/auth/gmail.readonly"
```

输出的 access token 仅用于短期 API 请求，禁止写入 Git、日志或截图。
