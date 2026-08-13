import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া (আপনার নিজস্ব চ্যানেল অপরিবর্তিত থাকবে)
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ২. যেসব প্লেলিস্ট যুক্ত করবেন তাদের গ্রুপের নাম, লোগো ও লিংক
playlists_to_add = [
    {
        "group_name": "Sony BD",
        "group_logo": "https://cdn.shortpixel.ai/spai/q_glossy+ret_img+to_webp/www.bizasialive.com/wp-content/uploads/2020/05/899ec721-sonylivnew001.jpg",
        "url": "http://140.245.107.220:5001/channels?url=https://ranapk-playlist.site/SONYBD.php"
    },
    {
        "group_name": "Toffee BD",
        "group_logo": "https://cdn.aptoide.com/imgs/d/e/c/dec7398ec8030c41f581dab8c64a7876_fgraphic.jpg",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/refs/heads/main/toffee_playlist.m3u"
    },
    {
        "group_name": "AKASH",
        "group_logo": "https://play-lh.googleusercontent.com/uH9MF_XcFR3-my7Z2o9w69j_glfMasPgks94-d3F610zWq8_FIgbYvr-FP1LSmpl_xmebuhoJHiMEytxEq86g",
        "url": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash-direct.m3u"
    },
    {
        "group_name": "BDIX TV",
        "group_logo": "https://play-lh.googleusercontent.com/ZhYHS7gw0U3RZHv6Gz48wK1DhC7GyXiyrIPZj1lDkbVn7OpqsQgocwrjEz1KGHUOpA",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/SM_bdix.m3u"
    },
    {
        "group_name": "RoarZone",
        "group_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxi69-tRSPLQhCnKqySLe-Gw_0C9CN6IFTMHtSyIKgzyOuqhzs1BSyA&s=10",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.m3u"
    },
    {
        "group_name": "BDIX",
        "group_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8glauz9GgWYPJC4N4_aW6kmdU-PF44jXRTI0vpGxd23i27VHCdFRMs=10",
        "url": "https://xtreamcode.allinonereborn.workers.dev/get.php?username=ratulhasanSa_246&password=1m43mozx&type=m3u_plus"
    },
    {
        "group_name": "AlixBD",
        "group_logo": "https://i.ibb.co/3kM0X8f/AlixBD-tv.png",
        "url": "http://alixbd.com/2022.m3u"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

all_external_channels = []

# ৩. প্রতিটি লিংক থেকে চ্যানেল এনে নির্দিষ্ট গ্রুপের নাম ও ক্যাটাগরি লোগো সেট করা
for item in playlists_to_add:
    group_name = item["group_name"]
    group_logo = item.get("group_logo", "")
    url = item["url"]

    if not url:
        continue

    try:
        response = requests.get(url, headers=headers, timeout=25)
        if response.status_code == 200:
            playlist_text = response.text
        else:
            continue
    except Exception as e:
        continue

    for line in playlist_text.splitlines():
        line_str = line.strip()

        if not line_str or line_str.startswith('#EXTM3U'):
            continue

        if line_str.startswith('#EXTINF'):
            # পুরনো সব গ্রুপ ট্যাগ মুছে ফেলা
            line_str = re.sub(r'group-title="[^"]*"', '', line_str)
            line_str = re.sub(r'tvg-group="[^"]*"', '', line_str)
            line_str = re.sub(r'group-title=\S+', '', line_str)
            line_str = re.sub(r'group-logo="[^"]*"', '', line_str)

            # ক্যাটাগরি বা গ্রুপের লোগো (group-logo) এবং গ্রুপ নেম ডাইরেক্ট বসিয়ে দেওয়া
            logo_attr = f' group-logo="{group_logo}"' if group_logo else ''
            
            if ',' in line_str:
                parts = line_str.split(',', 1)
                line_str = f'{parts[0].strip()} group-title="{group_name}"{logo_attr},{parts[1]}'
            else:
                line_str = f'{line_str} group-title="{group_name}"{logo_attr}'

        all_external_channels.append(line_str)

# ৪. ফাইল একত্র করে সেভ করা
external_content = "\n".join(all_external_channels)
final_content = f"{my_playlist}\n\n{external_content}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("All 7 Playlists updated with Group Logos successfully!")
