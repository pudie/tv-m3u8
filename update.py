import requests
from datetime import datetime

# JSON 地址
JSON_URL = "http://141.164.53.195/live/korea-live.json"
OUTPUT = "korea.m3u8"

# 请求头，避免部分源返回 403
HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def is_valid_m3u8(url):
    """判断 m3u8 URL 是否有效"""
    try:
        r = requests.head(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )
        if r.status_code in (401, 403, 404):
            return False
        return True
    except Exception:
        return False

def run():
    try:
        r = requests.get(JSON_URL, timeout=20)
        r.encoding = "utf-8"
        data = r.json()
    except Exception as e:
        print(f"{datetime.now()} 获取 JSON 失败: {e}")
        return

    lines = ["#EXTM3U"]
    count = 0

    for item in data:
        name = item.get("name", "").strip()
        uris = item.get("uris", [])

        if not name or not uris:
            continue

        valid_url = ""

        for u in uris:
            u = u.strip()
            if not u.lower().endswith(".m3u8"):
                continue

            if is_valid_m3u8(u):
                valid_url = u
                break

        if not valid_url:
            continue

        # DIYP 影音 APP 兼容格式
        lines.append(f"{name},{valid_url}")
        count += 1

        print(f"{datetime.now()} 有效频道: {name}")

    try:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{datetime.now()} 生成频道数量: {count}")
    except
