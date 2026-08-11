import urllib.request

# ১. আপনার tv.m3u ফাইলের কন্টেন্ট পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read()
except Exception as e:
    my_playlist = "#EXTM3U\n"

# ২. AlixBD এর লাইভ প্লেলিস্ট থেকে চ্যানেল টেনে আনা
alix_url = "https://alixbd.com/2022.m3u"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    req = urllib.request.Request(alix_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        alix_playlist = response.read().decode('utf-8')
except Exception as e:
    alix_playlist = ""

# ৩. দুটো প্লেলিস্টকে ফিল্টার করে একসাথে জোড়া দেওয়া
alix_lines = alix_playlist.splitlines()
alix_channels = []

for line in alix_lines:
    if line.strip() and not line.startswith('#EXTM3U'):
        alix_channels.append(line)

alix_content = "\n".join(alix_channels)

# ৪. দুটো প্লেলিস্ট যুক্ত করে ফাইনাল M3U তৈরি
final_playlist = my_playlist.strip() + "\n\n" + alix_content

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_playlist)

print("Playlist successfully merged and updated!")
