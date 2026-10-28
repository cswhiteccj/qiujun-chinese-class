# Google Cloud 語音服務整合｜安全部署清單（草稿）

目標：將 Google Cloud 專案 `notional-media-293807` 與現有學生端 GitHub Pages、Supabase Edge Functions、Gemini 架構整合。

> 目前尚未確認專案計費、Speech-to-Text API、Text-to-Speech API 的啟用狀態。**不得將此文件視為已完成部署。**

## 操作順序

1. [檢查計費](https://console.cloud.google.com/billing?project=notional-media-293807)，確認連結有效計費帳戶；先設定預算通知、配額及測試上限。預算通知**不是**硬性支出上限。
2. [啟用 Speech-to-Text](https://console.cloud.google.com/apis/library/speech.googleapis.com?project=notional-media-293807)。
3. [啟用 Text-to-Speech](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com?project=notional-media-293807)。
4. [服務帳戶](https://console.cloud.google.com/iam-admin/serviceaccounts?project=notional-media-293807) 建立 `qiujun-speech-backend`，不要授予 Owner/Editor。給予僅供呼叫語音 API 的最小權限；必要時以測試呼叫驗證具體 IAM 權限。避免建立長效 JSON 私鑰。
5. 後端身分：優先評估由支援 Workload Identity Federation (OIDC) 的可信工作負載交換短效權杖。**不得假定 Supabase Edge Functions 可直接充當已受 Google 信任的 OIDC identity provider。** 若無合適受信任 OIDC，採部署在 Google Cloud Run 的私有語音代理，並設計 Supabase 到代理的安全呼叫驗證，避免未受保護的公開端點。
6. 在 Supabase 建立私人 Storage bucket 存放學生錄音，使用授權規則限制本人與教師存取；服務端檢查 MIME、內容、長度與大小。MP4 在後端擷取音訊，禁止學生任意指定外部 URL 讓服務抓取。
7. Edge Function 驗證學生身分、作業權限、大小／時間限制、每日配額；只將受信任的錄音交給語音服務。服務端存放任務與結果，避免將 Google token 或 Supabase service_role 暴露給瀏覽器。
8. 中文語音辨識：試驗 `cmn-Hant-TW` 支援的模型／地區組合（不要假設同一 model 所有 region 可用）。超過同步 API 限額的長錄音須使用非同步模式及符合服務規格的儲存位置。
9. TTS：選擇台灣華語語音並比較品質；教師可審核音檔。禁止用 STT 逐字信心值直接當聲母、韻母、聲調評分。
10. 發音診斷：先做全文對齊／漏讀／重讀／可理解度等初步回饋，聲調與音素級回饋須聲學分析與教師複核；結果標明信心、不確定性。附逐句時間戳、原音重播、教師修改權。
11. 上線前測試：1 分鐘內 MP3、較長 MP3、含影音 MP4、無權限存取、無效檔案、聲調變調、網路故障、帳單保護、刪除錄音、費用觀測。

## 安全與隱私

- 不將 Google service-account JSON 或 API key 放到 GitHub、GitHub Pages、前端 VITE 變數、公開訊息。
- 不接受未驗證的學生直接呼叫需要計費的 Google 服務。
- 不將學生錄音設為公開；設定保存與刪除機制，告知學生用途與存取權限。
- Google Cloud IAM 的 Workload Identity Federation 為優先模式，但必須先核對外部身分來源實際能力；若需使用私鑰，應視為例外並定期輪替。

參考：
- https://docs.cloud.google.com/speech-to-text/docs/setup
- https://docs.cloud.google.com/text-to-speech/docs/get-started
- https://docs.cloud.google.com/iam/docs/workload-identities
- https://docs.cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
