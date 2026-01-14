import requests
from datetime import datetime

# JSON 地址
JSON_URL = "http://141.164.53.195/live/korea-live.json"

OUTPUT1 = "korea.m3u8"   # DIYP 影音 APP 格式
OUTPUT2 = "korea2.m3u8"  # EXTINF 两行标准格式

def run():
    try:
        r = requests.get(JSON_URL, timeout=20)
        r.encoding = "utf-8"
        data = r.json()
    except Exception as e:
        print(f"{datetime.now()} 获取 JSON 失败: {e}")
        return

    # 文件1：DIYP 影音 APP 格式
    lines1 = ["#EXTM3U"]

    # 文件2：EXTINF 两行格式
    lines2 = ["#EXTM3U"]

    count = 0

    for item in data:
        name = item.get("name", "").strip()
        uris = item.get("uris", [])

        if not name or not uris:
            continue

        # 只接受以 .m3u8 结尾的 URL
        url = ""
        for u in uris:
            u = u.strip()
            if u.lower().endswith(".m3u8"):
                url = u
                break

        if not url:
            continue

        # ---------- 文件1：DIYP 格式 ----------
        # 频道名,URL
        lines1.append(f"{name},{url}")

        # ---------- 文件2：EXTINF 标准格式 ----------
        lines2.append(f"#EXTINF:-1 ,{name}")
        lines2.append(url)

        count += 1

    try:
        with open(OUTPUT1, "w", encoding="utf-8") as f1:
            f1.write("\n".join(lines1))

        with open(OUTPUT2, "w", encoding="utf-8") as f2:
            f2.write("\n".join(lines2))

        print(f"{datetime.now()} 生成频道数量: {count}")
        print(f"{datetime.now()} 已生成文件: {OUTPUT1}, {OUTPUT2}")

    except Exception as e:
        print(f"{datetime.now()} 写入文件失败: {e}")

if __name__ == "__main__":
    run()
