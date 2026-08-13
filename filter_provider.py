import json
import re
import requests

PORTAL_URL = "https://alex.rocktv.be/stalker_portal/c/"
MAC_ADDR = "00:1A:79:8C:0E:A7"
DEVICE_ID = "C4B0C9CA57DE7DAF4676BEEA9205402B11DD69C447496326F2CEC69AD1997460"
SERIAL_NUM = "B96257E7F728E"

headers = {
    'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stalkerphp/2.0.0 Safari/533.3',
    'X-User-Agent': 'Model: MAG250; Link: WiFi',
    'Cookie': f'mac={MAC_ADDR}; stb_lang=en; timezone=Europe%2FLondon',
    'Referer': PORTAL_URL
}

session = requests.Session()

def stalker_request(action, params=""):
    url = f"{PORTAL_URL}portal.php?type=itv&action={action}&{params}"
    try:
        res = session.get(url, headers=headers, timeout=15)
        return res.json()
    except Exception as e:
        print(f"Error action {action}: {e}")
        return None

# ১. হ্যান্ডশেক এবং টোকেন গ্রহণ
handshake = stalker_request("handshake")
if handshake and 'js' in handshake and 'token' in handshake['js']:
    token = handshake['js']['token']
    headers['Authorization'] = f"Bearer {token}"

# ২. ক্যাটাগরি (Genre) লিস্ট আনা
genres = stalker_request("get_genres")
target_genre_ids = []

if genres and 'js' in genres:
    for g in genres['js']:
        title = str(g.get('title', '')).upper()
        # HINDI, KIDS এবং KIDS 24/7 আইডি সিলেক্ট করা
        if "HINDI" in title and "NEWS" not in title:
            target_genre_ids.append(str(g.get('id')))
        elif title == "KIDS" or "KIDS 24/7" in title or "KIDS | 24/7" in title:
            target_genre_ids.append(str(g.get('id')))

m3u_lines = ["#EXTM3U"]

# ৩. সিলেক্টেড ক্যাটাগরি থেকে চ্যানেল আনা
for genre_id in target_genre_ids:
    channels = stalker_request("get_ordered_list", f"genre={genre_id}&force_ch_link_check=1")
    if channels and 'js' in channels and 'data' in channels['js']:
        for ch in channels['js']['data']:
            ch_name = ch.get('name', '')
            ch_cmd = ch.get('cmd', '')
            ch_genre = ch.get('tv_genre_id', '')
            
            # BEN 10 ফিল্টারিং (যদি KIDS 24/7 সেকশনের হয়)
            is_ben10 = "BEN 10" in ch_name.upper() or "BEN10" in ch_name.upper()
            
            # M3U ফরম্যাটে স্ট্রিম লিংক তৈরি
            if ch_cmd:
                stream_id = ch_cmd.replace('ffmpeg ', '')
                stream_url = f"{PORTAL_URL}cmd/{stream_id}"
                
                extinf = f'#EXTINF:-1 group-title="Stalker Channels",{ch_name}'
                m3u_lines.append(extinf)
                m3u_lines.append(stream_url)

# ৪. ফাইল সেভ করা
with open('filtered_channels.m3u', 'w', encoding='utf-8') as f:
    f.write("\n".join(m3u_lines))

print("Stalker Portal ফিল্টারিং সম্পন্ন হয়েছে!")
