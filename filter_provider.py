import os
import re
import requests

PORTAL_URL = "https://alex.rocktv.be/stalker_portal/c/"
MAC_ADDR = "00:1A:79:8C:0E:A7"
DEVICE_ID = "C4B0C9CA57DE7DAF4676BEEA9205402B11DD69C447496326F2CEC69AD1997460"
SERIAL_NUM = "B96257E7F728E"

# 1. MAG250 প্লেয়ার অনুকরণে স্পেশাল হেডার
headers = {
    'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stalkerphp/2.0.0 Safari/533.3',
    'X-User-Agent': 'Model: MAG250; Link: WiFi',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': f'mac={MAC_ADDR}; stb_lang=en; timezone=Europe%2FLondon',
    'Referer': PORTAL_URL
}

session = requests.Session()

def api_call(action, extra_params=""):
    url = f"{PORTAL_URL}portal.php?type=itv&action={action}&{extra_params}"
    try:
        res = session.get(url, headers=headers, timeout=20)
        return res.json()
    except Exception as e:
        print(f"[-] Error calling action '{action}': {e}")
        return None

print("[+] Connecting to Stalker Portal...")

# 2. সেশন হ্যান্ডশেক (Handshake)
hs_data = api_call("handshake")
token = None

if hs_data and 'js' in hs_data and 'token' in hs_data['js']:
    token = hs_data['js']['token']
    headers['Authorization'] = f"Bearer {token}"
    print(f"[+] Handshake successful! Token obtained.")
else:
    print("[-] Handshake failed or server blocked standard request.")

# 3. প্রোফাইল লোড (Profile Load)
profile = api_call("get_profile", f"hd=1&sn={SERIAL_NUM}&device_id={DEVICE_ID}&device_id2={DEVICE_ID}")

# 4. সমস্ত ক্যাটাগরি/জেনারস ফেচ করা
genres_data = api_call("get_genres")
target_genres = {}

if genres_data and 'js' in genres_data:
    for g in genres_data['js']:
        g_id = str(g.get('id'))
        g_title = str(g.get('title', '')).strip().upper()
        
        # আপনার কাঙ্ক্ষিত ক্যাটাগরি ফিল্টার: HINDI, KIDS, KIDS 24/7
        is_hindi = ("HINDI" in g_title) and ("NEWS" not in g_title)
        is_kids = ("KIDS" in g_title)
        
        if is_hindi or is_kids:
            target_genres[g_id] = g_title
            print(f"[+] Found Target Category: ID {g_id} -> {g_title}")

m3u_lines = ["#EXTM3U"]
total_added = 0

# 5. চ্যানেলগুলো ফেচ করে ফিল্টার করা
for g_id, g_title in target_genres.items():
    ch_data = api_call("get_ordered_list", f"genre={g_id}&force_ch_link_check=1")
    
    if ch_data and 'js' in ch_data and 'data' in ch_data['js']:
        for ch in ch_data['js']['data']:
            ch_id = ch.get('id')
            ch_name = ch.get('name', '').strip()
            ch_cmd = ch.get('cmd', '')
            
            name_upper = ch_name.upper()
            
            # বেন টেন ফিল্টারিং লজিক
            is_kids_247 = "24/7" in g_title or "24/7" in name_upper
            if is_kids_247:
                # যদি কিডস ২৪/৭ ক্যাটাগরি হয়, তবে শুধু Ben 10 চ্যানেলগুলো রাখবে
                if not ("BEN 10" in name_upper or "BEN10" in name_upper):
                    continue

            # ক্রিয়েটিং ডাইনামিক চ্যানেল প্লেব্যাক লিংক
            if ch_cmd:
                stream_cmd = ch_cmd.replace('ffmpeg ', '').strip()
                play_url = f"{PORTAL_URL}cmd/{stream_cmd}"
                
                m3u_lines.append(f'#EXTINF:-1 group-title="{g_title}",{ch_name}')
                m3u_lines.append(play_url)
                total_added += 1

# 6. ফাইল সেভ করা
with open('filtered_channels.m3u', 'w', encoding='utf-8') as f:
    f.write("\n".join(m3u_lines))

print(f"[SUCCESS] Total {total_added} channels collected and saved into 'filtered_channels.m3u'")
