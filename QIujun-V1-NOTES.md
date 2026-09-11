# 秋君老師的華語教學 V1

此版本以 InterAct v1.2.17 為基礎進行個人教學用途的第一階段客製化。

## 已完成
- 前台品牌改為「秋君老師的華語教學」 / Teacher Qiujun’s Chinese Class
- 首頁文字簡化為「互動、練習、即時回饋」
- 教師端「場次」主要操作文字改為「課堂」
- Windows 產品名稱與 appId 客製化
- Excel 課堂報告品牌與檔名客製化
- 學生 Join / Participant 頁移除原作者個人社群按鈕
- QR Code fallback 不再指向原作者 GitHub Pages；正式部署前請設定 VITE_PUBLIC_APP_URL 或後端 appUrl

## 特別保留
原專案的 LICENSE、原作者資訊與必要 attribution 未刪除。請依 PolyForm Noncommercial 1.0.0 使用與散布。

## 下一階段建議
1. 建立自己的 Supabase 專案與 Edge Functions。
2. 部署自己的學生 Web App，設定 VITE_PUBLIC_APP_URL。
3. 重整教師課堂控制頁為「出題 / 課堂互動 / AI 教學」三區。
4. 新增華語專用發音分析維度（聲母、韻母、聲調、語速、流暢度）。
5. 新增 A1/A2/B1 AI 出題設定。
