import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া (আপনার নিজস্ব গ্রুপ অপরিবর্তিত থাকবে)
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ২. সোনি প্লেলিস্টের URL
sony_url = "http://140.245.107.220:5001/channels?url=https://ranapk-playlist.site/SONYBD.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(sony_url, headers=headers, timeout=20)
    if response.status_code == 200:
        sony_text = response.text
    else:
        sony_text = ""
except Exception as e:
    sony_text = ""

# ৩. সকল পুরানো গ্রুপ ট্যাগ মুছে ফেলে নতুন করে 'Sony BD' গ্রুপ সেট করা
sony_lines = []
for line in sony_text.splitlines():
    line_str = line.strip()
    
    if not line_str or line_str.startswith('#EXTM3U'):
        continue

    if line_str.startswith('#EXTINF'):
        # পুরানো যেকোনো group-title বা tvg-group সম্পুর্ন মুছে ফেলা
        line_str = re.sub(r'group-title="[^"]*"', '', line_str)
        line_str = re.sub(r'tvg-group="[^"]*"', '', line_str)
        line_str = re.sub(r'group-title=\S+', '', line_str)
        
        # চ্যানেল নামের আগে একবারে পরিচ্ছন্নভাবে group-title="Sony BD" যুক্ত করা
        if ',' in line_str:
            parts = line_str.split(',', 1)
            line_str = f"{parts[0].strip()} group-title=\"Sony BD\",{parts[1]}"
        else:
            line_str = f"{line_str} group-title=\"Sony BD\""

    sony_lines.append(line_str)

sony_channels = "\n".join(sony_lines)

# ৪. ফাইল একত্র করে সেভ করা
final_content = f"{my_playlist}\n\n{sony_channels}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Cleaned up old groups and set Sony BD group successfully!")
