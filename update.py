import requests
from datetime import datetime

JSON_URL = "http://141.164.53.195/live/korea-live.json"

OUTPUT1 = "korea.m3u8"
OUTPUT2 = "korea2.m3u8"

def extract_m3u8(uris):
    """从各种 uris 结构中提取 m3u8"""
    if isinstance(uris, list):
        for u in uris:
            if isinstance(u, str) and u.lower().endswith(".m3u8"):
                return u.strip()

    elif isinstance(uris, dict):
        for u in uris.values():
            if isinstance(u, str) and u.lower().endswith(".m3u8"):
                return u.strip()

    elif isinstance(uris, str):
        if uris.lower().endswith(".m3u8"):
            return uris.strip()

    return None

def run():
    try:
        r = requests.get(JSON_URL, timeout=20)
        r.encoding = "utf-8"
        data = r.json()
    except Exception as e:
        print(f"{datetime.now()} 获取 JSON 失败: {e}")
        return

    lines1 = ["#EXTM3U"]
    lines2 = ["#EXTM3U"]

    count = 0

    for item in data:
        name = item.get("name", "").strip()
        uris = item.get("uris")

        if not name or not uris:
            continue

        url = extract_m3u8(uris)
        if not url:
            continue

        # DIYP 格式
        lines1.append(f"{name},{url}")

        # 标准 EXTINF 两行
        lines2.append(f"#EXTINF:-1,{name}")
        lines2.append(url)

        count += 1

    with open(OUTPUT1, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines1))

    with open(OUTPUT2, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines2))

    print(f"{datetime.now()} 生成频道数量: {count}")
    print(f"{datetime.now()} 已生成文件: {OUTPUT1}, {OUTPUT2}")

if __name__ == "__main__":
    run()
