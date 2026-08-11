import requests

# ১. আপনার tv.m3u ফাইলের নিজস্ব চ্যানেল পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ২. সোনি প্লেলিস্টের নতুন URL
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

# ৩. #EXTM3U লাইন বাদ দিয়ে চ্যানেল কন্টেন্ট সংগ্রহ করা
sony_lines = []
for line in sony_text.splitlines():
    if line.strip() and not line.strip().startswith('#EXTM3U'):
        sony_lines.append(line)

sony_channels = "\n".join(sony_lines)

# ৪. নিজস্ব চ্যানেল ও নতুন সোনি প্লেলিস্ট মার্জ করে সেভ করা
final_content = f"{my_playlist}\n\n{sony_channels}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Sony Playlist updated successfully!")
