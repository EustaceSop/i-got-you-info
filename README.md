找到你.py
=================================

本專案為一個用 Python 撰寫的簡易資訊收集器，展示如何從本地文件中擷取 Discord Token、解析對應使用者 ID，以及查詢目前的 IP 地理資訊，並將其發送至 Discord Webhook。**本程式已不再從系統中讀取任何 License Key 或個人授權資料。**

🔍 功能簡介
-------------

1. **擷取 Discord Token：**
   - 掃描本機瀏覽器（預設為 Chrome）資料目錄中的 LevelDB 檔案，透過正規表示式尋找可能的 Discord Token。
2. **解碼使用者 ID：**
   - Token 的第一段會以 base64 解碼，取得對應使用者 ID。
3. **查詢 IP 與地理位置：**
   - 使用 bilibili 提供的公開 API 查詢目前裝置的 IP 地址、城市、國家、ISP 和座標位置，並提供 Google Maps 定位連結。
4. **資訊彙整並發送至 Discord Webhook：**
   - 將 Token 與 IP 位置整合為 Discord embed 格式，透過 POST 請求傳送。

📦 使用到的工具與 API
------------------------

- `requests`: 發送 HTTP 請求。
- `urllib.request`: 傳統 POST 請求方式。
- `re`, `base64`, `os`, `json`: Python 標準函式庫。
- **Bilibili 公開 API**：查詢 IP 位置信息。
- **MyMemory 翻譯 API**：將地名翻譯為英文（從簡體中文）。

🛡️ 如何防範 Token 被擷取
---------------------------

若您是 Discord 使用者，為了避免帳號安全風險，請注意以下事項：

1. **切勿將 Token 外洩**：Discord Token 相當於帳號密碼的替代品，擁有者可以完全控制帳號。
2. **不要在不明網站登入或安裝來源不明的軟體。**
3. **開啟雙重身份驗證（2FA）**：就算 Token 被竊，也能阻擋未授權登入行為。
4. **定期檢查 Discord 帳戶授權與登入紀錄。**
5. **使用防毒軟體與惡意程式掃描工具。**
6. **避免將本地應用存取資料存入未加密的檔案中。**

⚠️ 強化版免責聲明
------------------

> 本程式僅供學術研究與資訊安全學習用途，**不得用於任何未經授權的資料擷取、駭客行為或侵犯隱私**。使用者須自行承擔所有使用後果，作者不對任何違法用途負責。本專案未收集、儲存或傳送任何使用者敏感資訊，且對程式行為皆公開透明。

🔧 安裝與執行方式
------------------

1. 安裝 Python 套件（需要 Python 3.6+）：

    pip install requests

2. 執行：

    python cleaned_ip_info_collector.py

請在可存取 Chrome LevelDB 檔案的環境下執行（例如本機 Windows）。

🙌 貢獻來源
------------

- [Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api)：IP 查詢 API。
- [piotr-ginal/discord-token-grabber](https://github.com/piotr-ginal/discord-token-grabber)：Discord Token 擷取與解析的邏輯參考。
