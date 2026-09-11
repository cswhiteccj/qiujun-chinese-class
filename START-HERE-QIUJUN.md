# 秋君老師的華語教學 V3｜先看這份

這個版本以 InterAct 原始專案為底，已改造成「秋君老師的華語教學」個人課堂系統，定位為教師本人帶國際學生上華語課使用。

## V3 已完成的核心系統

### 教師端
- 建立／管理課堂與 QR Code 加入
- 截圖派題、圖片派題、文字派送、檔案收件
- 手動純文字出題，不需要先截圖
- AI 華語出題：A1、A2、B1、B2
- AI 題型：選擇、是非、句子重組、詞語填空、配對、簡答／造句、口語回答、發音練習
- AI 題目先預覽、可修改題目、選項與答案鍵，再派送
- 本機華語題庫：儲存、搜尋、程度篩選、刪除、直接派送
- 題庫 JSON 匯入／匯出，可備份或換電腦
- 彈幕、文字雲、抽籤、搶答、Exit Ticket
- 即時字幕與即時口譯（依原專案 Plus／API 設定）
- 課後 AI 報告與 Excel 匯出

### 學生端
- 手機瀏覽器掃 QR Code 加入，不需安裝
- 繁中、英文、越南文、印尼文、日文、韓文切換；未翻到的次要文字回退英文
- 題型：選擇題、是非題、句子重組、詞語填空、配對題、簡答／造句、口語、發音、看圖選擇、看圖說話、檔案上傳
- 句子重組保留重複詞並依順序判分
- 填空依空格順序判分
- 配對依配對關係判分

### AI 華語能力
- 出題分級 A1–B2，不只是換難字，而是依認知與語用任務分級
- 發音回饋特別檢視聲母、韻母、聲調／變調、輕聲、語流、停頓、流暢度與可理解度
- 純文字口語／發音題不再依賴圖片
- 客觀 AI 題帶答案鍵，停止作答後自動判分

## 部署時一定要設定

前端 `.env`：
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_PUBLIC_APP_URL`（學生 QR Code 要連到你自己的學生網站）

Supabase Edge Functions secrets：
- `GEMINI_API_KEY`（AI 出題、分析、發音等）
- 原專案其他 AI／短網址功能如要使用，依 `supabase/.env.example` 與原 README 再設定對應金鑰

新增的 Edge Function：
- `generate-chinese-questions`

部署 Supabase 時要一起部署這個 function。它已做 presenter token 驗證，不能讓一般學生直接消耗你的 Gemini API。

## 建置

原專案使用 pnpm：

```bash
pnpm install
pnpm build
```

Windows 打包：

```bash
pnpm desktop:package
```

本次工作環境沒有外網，無法下載 pnpm/node_modules，所以無法完成 production build。已用全域 TypeScript 對新增／修改檔案做語法層檢查，沒有發現 TS1xxx 語法解析錯誤；完整型別與 production build 仍需要在可連 npm registry 的電腦上執行。

## 授權

原專案採 PolyForm Noncommercial 1.0.0。此版本保留 LICENSE 與原專案 attribution。前台品牌可以是「秋君老師的華語教學」，但不能把法律上的原作者／授權資訊當成不存在。

---

## 目前採用的正式部署方案（V3.1）

- 學生端：GitHub Pages
- 後端：秋君老師自己的 Supabase Project
- AI 與語音：Gemini
- OpenAI：不使用
- 即時語音：Gemini 語音轉寫、字幕與多語文字翻譯
- 學生端語音口譯輸出：V3.1 暫不啟用，以保持系統簡潔與單一 AI 供應商

詳細步驟請看 `GITHUB-SUPABASE-SETUP.md`。
