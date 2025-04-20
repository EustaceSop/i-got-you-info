
I GOT YOU
=================================

本專案為一個用 Python 撰寫的簡易資訊收集器，目的是展示如何從本地文件中擷取 Discord Token，解析對應的使用者 ID，以及查詢當前電腦的 IP 地理資訊。所有結果會被送至指定的 Discord Webhook。

🔍 專案原理
------------
此工具會執行以下幾個動作：

1. 從瀏覽器的本地資料中掃描 Discord Token
   - 掃描目標資料夾（如 Chrome 的 leveldb）以正規表示式找出可能的 Discord Token。
2. 從 Token 解碼出使用者 ID
   - Token 的第一段是 base64 編碼的使用者 ID。
3. 查詢 IP 與地理位置
   - 使用 bilibili 公開 API 查詢當前 IP 的詳細位置（國家、省份、城市、ISP、座標等），並提供 Google Maps 連結。
4. 抓取暫存資料中的 License Key
   - 嘗試從 %TEMP%\data 中讀取 JSON 結構以取得 license key。
5. 將所有資訊發送至 Discord Webhook
   - 格式化為 Discord embed，並透過 POST 請求發送。

📦 使用到的工具/庫
------------------

- requests: 用於發送 HTTP 請求。
- urllib.request: 傳統方式執行 POST 請求。
- base64, re, json, os: 標準庫，用於資料處理。
- Bilibili API: 查詢 IP 地理資訊。
- MyMemory Translation API: 將中文地名翻譯為英文。

⚠️ 免責聲明
-----------

本程式碼僅供學術研究與技術學習用途，以及展示Discord的資安漏洞，請勿用於任何未經授權或侵犯他人隱私的用途。使用者需自行承擔使用此工具所造成的任何法律後果與責任。

🔧 安裝與執行
-------------

### 安裝依賴套件

請先確認已安裝 Python 3.6+，然後安裝 requests：

    pip install requests

### 執行方式

    python ip.py

若你想讓其在背景自動收集資料，請注意必須執行在能夠讀取使用者瀏覽器資料夾的環境中（如 Windows 本機）。

🙌 貢獻來源
-----------

- Nemo2011/bilibili-api: IP 位置查詢接口靈感。
- piotr-ginal/discord-token-grabber: 掃描並解碼 Discord Token 的方法與思路參考。
