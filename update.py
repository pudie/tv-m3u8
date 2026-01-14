import requests
from datetime import datetime

JSON_URL = "http://141.164.53.195/live/korea-live.json"
OUTPUT = "korea.m3u8"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_valid_m3u8(url):
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

        lines.append(f"{name},{valid_url}")
        count += 1

    try:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{datetime.now()} 生成频道数量: {count}")
    except Exception as e:
        print(f"{datetime.now()} 写入文件失败: {e}")

if __name__ == "__main__":
    run()
