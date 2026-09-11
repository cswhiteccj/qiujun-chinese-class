# 秋君老師的華語教學：GitHub + Supabase + Gemini 部署

## 已採用的架構

- 學生端：GitHub Pages
- 教師端：Windows Electron App
- 後端：你自己的 Supabase Project
- AI：Gemini
- 即時語音轉寫／字幕／文字翻譯：Gemini
- OpenAI：不需要

## GitHub repository 建議名稱

`qiujun-chinese-class`

GitHub Pages 部署工作流程已放在：

`.github/workflows/deploy.yml`

推送到 `main` 後會自動 build 並部署學生端。

## GitHub Repository Variables

Repository → Settings → Secrets and variables → Actions → Variables，建立：

- `VITE_SUPABASE_URL`：例如 `https://xxxxxxxxxxxxxxxxxxxx.supabase.co`
- `VITE_SUPABASE_ANON_KEY`：Supabase 的 publishable key
- `VITE_PUBLIC_APP_URL`：最後的 GitHub Pages 網址，例如 `https://YOUR_GITHUB_NAME.github.io/qiujun-chinese-class`

這三個值會放進學生端前端；只能使用 Supabase publishable/anon key，絕對不要放 service_role 或 secret key。

## Supabase

不需要下載 Supabase App。直接使用瀏覽器登入 Supabase Dashboard 即可。

建立 Project 後，教師桌面版可以使用「系統設定 → 還沒建立後端？讓系統協助部署」，填入：

1. Project ID
2. Publishable key
3. Supabase Access Token（只在自動部署時使用，不儲存）
4. Gemini API key

自動部署會建立資料表、Storage、Edge Functions 與管理金鑰。

## Gemini

Supabase Edge Function secret：

`GEMINI_API_KEY`

AI 出題、課堂分析、發音／口語分析、即時字幕與多語文字翻譯都走 Gemini。

`OPENAI_API_KEY` 已從新版部署流程移除。

## GitHub Pages

第一次 push 後，GitHub repository → Settings → Pages，Source 選 GitHub Actions。

部署成功後，把實際 Pages URL 寫入 `VITE_PUBLIC_APP_URL`，重新觸發 Deploy workflow；教師 QR Code 就會導向你的學生端。

## Windows 教師版

`.github/workflows/release.yml` 會在建立 `v*` tag 時產生：

- `秋君老師的華語教學.exe`
- `秋君老師的華語教學.zip`

## 授權

本專案衍生自 InterAct，原始 `LICENSE` 與必要 attribution 必須保留。前台品牌可使用「秋君老師的華語教學」。
