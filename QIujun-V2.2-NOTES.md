# 秋君老師的華語教學 V2.2

新增兩種華語互動題型：

## 詞語填空
- 教師輸入含 `＿＿` 或 `__` 的句子。
- 詞語選項可用換行、逗號或斜線分隔。
- 學生依序點選詞語填入空格，可重新填寫後送出。

## 配對題
- 教師每行輸入一組配對，例如 `老師＝teacher`。
- 可使用 `＝`、`=`、`→` 或 `->` 分隔。
- 學生先選左側，再選右側完成配對；右側會自動打亂。
- 支援重新配對後送出。

同步更新 QuestionType、Supabase schema/migration、presenter-action、參與統計、課堂報告與 Excel 題型名稱。

資料庫 migration：`supabase/migrations/202609070002_add_word_fill_and_matching.sql`
