# Qiujun Chinese Class V3 Complete Notes

## 本版新增
1. AI 華語出題 Modal：A1/A2/B1/B2、混合或指定題型、1–10 題、主題與教師補充要求。
2. AI 題目預覽：教師可修改題幹、選項、答案鍵後才派送。
3. 題庫：localStorage 儲存、程度篩選、搜尋、匯入、匯出、刪除、直接派送。
4. 手動純文字出題：不再依賴截圖。
5. presenter-action 新增 `create_text_question`。
6. 客觀題停止作答時自動判分；句子重組、詞語填空、配對採各自正確的比較邏輯。
7. 新增 `generate-chinese-questions` Supabase Edge Function，並用 presenter token 驗證保護 Gemini API。
8. 純文字 pronunciation / oral_response 支援：錄音分析不再要求 screenshot。
9. 華語發音 AI prompt 改為聲母、韻母、聲調／變調、輕聲、語流、停頓與流暢度導向。
10. 學生語言加入 vi、id、ja、ko，重要操作有翻譯，其他文案回退英文。
11. 產品 package 更新為 `qiujun-chinese-class` 3.0.0。
12. 主要前台 InterAct 品牌字樣進一步改為「秋君老師的華語教學」，保留技術名稱與授權 attribution。

## 主要新增檔案
- `src/components/AiChineseQuestionModal.tsx`
- `src/components/QuestionBankModal.tsx`
- `src/lib/questionBank.ts`
- `supabase/functions/generate-chinese-questions/index.ts`
- `START-HERE-QIUJUN.md`

## 還需要實機驗證
- `pnpm install && pnpm build`
- 建立測試 Supabase 專案並執行既有 migrations
- 部署所有 Edge Functions（含 generate-chinese-questions）
- 實機測試 Windows Electron、手機 Safari/Chrome、麥克風權限與多語字幕／口譯
