import urllib.request

# ১. আপনার tv.m3u ফাইলের কন্টেন্ট পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read()
except Exception as e:
    my_playlist = "#EXTM3U\n"

# ২. AlixBD এর লাইভ প্লেলিস্ট থেকে অটো-আপডেট কন্টেন্ট রিড করা
alix_url = "https://alixbd.com/2022.m3u"
req = urllib.request.Request(alix_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        alix_playlist = response.read().decode('utf-8')
except Exception as e:
    alix_playlist = ""

# ৩. দুটো প্লেলিস্টকে একসাথে জোড়া দেওয়া
alix_channels = "\n".join([line for line in alix_playlist.splitlines() if not line.startswith('#EXTM3U')])

final_playlist = my_playlist + "\n\n" + alix_channels

# ৪. চূড়ান্ত অটো-আপডেট ফাইল হিসেবে playlist.m3u তে সেভ করা
with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_playlist)

print("Playlist auto-updated successfully!")
