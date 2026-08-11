import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া (এটিতে কোনো হাত দেওয়া হবে না)
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

# ৩. সোনি প্লেলিস্টের সকল চ্যানেলের গ্রুপ টাইটেল পরিবর্তন করে 'Sony BD' করা
sony_lines = []
for line in sony_text.splitlines():
    line_str = line.strip()
    
    # #EXTM3U মূল হেডার বাদ দেওয়া
    if not line_str or line_str.startswith('#EXTM3U'):
        continue

    # যদি লাইনটি চ্যানেলের ইনফরমেশন (#EXTINF) হয়
    if line_str.startswith('#EXTINF'):
        # আগে থেকে কোনো group-title থাকলে তা সরিয়ে ফেলা
        line_str = re.sub(r'group-title="[^"]*"', '', line_str)
        
        # নতুন গ্রুপ টাইটেল 'Sony BD' যুক্ত করা
        line_str = line_str.replace('#EXTINF:-1', '#EXTINF:-1 group-title="Sony BD"')
        line_str = line_str.replace('#EXTINF:0', '#EXTINF:0 group-title="Sony BD"')
        
        # যদি অন্য কোনো ফরম্যাটে থাকে তাও যেন group-title যুক্ত হয়
        if 'group-title=' not in line_str:
            line_str = line_str.replace('#EXTINF:', '#EXTINF: group-title="Sony BD" ')

    sony_lines.append(line_str)

sony_channels = "\n".join(sony_lines)

# ৪. নিজস্ব প্লেলিস্ট এবং পরিবর্তিত সোনি প্লেলিস্ট একত্র করা
final_content = f"{my_playlist}\n\n{sony_channels}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Sony BD group title applied successfully!")
