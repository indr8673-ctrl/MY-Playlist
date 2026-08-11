import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া (আপনার নিজস্ব চ্যানেল অপরিবর্তিত থাকবে)
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ২. যেসব প্লেলিস্ট যুক্ত করবেন তাদের গ্রুপের নাম ও লিঙ্ক
playlists_to_add = [
    {
        "group_name": "Sony BD",
        "url": "http://140.245.107.220:5001/channels?url=https://ranapk-playlist.site/SONYBD.php"
    },
    {
        "group_name": "Toffee BD",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/refs/heads/main/toffee_playlist.m3u"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

all_external_channels = []

# ৩. প্রতিটি লিঙ্ক থেকে চ্যানেল এনে গ্রুপের নাম ঠিক করা
for item in playlists_to_add:
    group_name = item["group_name"]
    url = item["url"]
    
    if not url:
        continue

    try:
        response = requests.get(url, headers=headers, timeout=20)
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
            # পুরানো সব গ্রুপ ট্যাগ মুছে ফেলা
            line_str = re.sub(r'group-title="[^"]*"', '', line_str)
            line_str = re.sub(r'tvg-group="[^"]*"', '', line_str)
            line_str = re.sub(r'group-title=\S+', '', line_str)
            
            # নতুন নির্দিষ্ট গ্রুপ নেম সেট করা
            if ',' in line_str:
                parts = line_str.split(',', 1)
                line_str = f'{parts[0].strip()} group-title="{group_name}",{parts[1]}'
            else:
                line_str = f'{line_str} group-title="{group_name}"'

        all_external_channels.append(line_str)

# ৪. ফাইল একত্র করে সেভ করা
external_content = "\n".join(all_external_channels)
final_content = f"{my_playlist}\n\n{external_content}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Sony BD and Toffee BD updated successfully!")
