import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ২. নিজস্ব নোটপ্যাড ক্যাটাগরি লোগো
my_category_logos = {
    "Kid": "https://www.shutterstock.com/image-vector/kids-text-logo-movie-editable-260nw-2536104593.jpg",
    "Entertainment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9sZttim5GLAbajaB_Jnq3xBGpj2hn3S1dOpLFU3M25kPK1dz28hOV3E4&s=10",
    "Movie": "https://thumbs.dreamstime.com/b/movie-text-logo-cinema-film-entertainment-industry-png-transparent-image-stylized-related-content-representing-films-364904222.jpg",
    "Sun": "https://e7.pngegg.com/pngimages/341/140/png-clipart-logo-brand-product-design-sun-direct-direct-sunlight-television-text.png",
    "Bangla Movie": "https://mir-s3-cdn-cf.behance.net/projects/404/97af8697707749.Y3JvcCw5ODYsNzcxLDEwMiwxODMz.jpg",
    "BD News": "https://yt3.googleusercontent.com/AQLUH_ixhkqBRCV9M1rtWRQhUFiXB1QvX-l1DIbrfmeMjrU8kJzAeCaiupHjEPEz9M2daSfm9A=s900-c-k-c0x00ffffff-no-rj",
    "Sony": "https://www.medianews4u.com/wp-content/uploads/2017/08/sony-liv-logo-1-3-2.jpg",
    "Sony LIV": "https://static.vecteezy.com/system/resources/previews/075/195/417/non_2x/sony-liv-logo-rounded-glossy-icon-with-transparent-background-free-png.png",
    "World": "https://www.shutterstock.com/image-vector/world-television-logo-template-design-260nw-1403727485.jpg",
    "English Movies": "https://i.pinimg.com/474x/bd/30/44/bd3044c117c29cb24fc00e9d94a09510.jpg",
    "Sports": "https://img.magnific.com/premium-vector/professional-tv-channel-logo-design-concept-vector-illustration_875240-1836.jpg?semt=ais_test_b&w=740&q=80",
    "ID News": "https://e7.pngegg.com/pngimages/3/57/png-clipart-india-news-news-broadcasting-television-news-television-logo.png",
    "Music": "https://static.vecteezy.com/system/resources/previews/021/813/091/non_2x/music-tv-logo-design-template-with-tv-icon-and-music-icon-perfect-for-business-company-mobile-app-restaurant-etc-free-vector.jpg",
    "Toffee": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/DNMXs5UBm1RY_In7IJ72/posters/737b5c6e-8435-4cd8-81de-16a499fa6f4e.png",
}

processed_my_playlist = []
for line in my_playlist.splitlines():
    line_str = line.strip()
    if line_str.startswith('#EXTINF'):
        match = re.search(r'group-title="([^"]+)"', line_str)
        if match:
            group_name = match.group(1)
            if group_name in my_category_logos:
                logo_url = my_category_logos[group_name]
                line_str = re.sub(r'group-logo="[^"]*"', '', line_str)
                line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" group-logo="{logo_url}"')
                if 'tvg-logo=""' in line_str:
                    line_str = line_str.replace('tvg-logo=""', f'tvg-logo="{logo_url}"')
                elif 'tvg-logo="' not in line_str:
                    line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" tvg-logo="{logo_url}"')
    processed_my_playlist.append(line_str)

my_playlist_updated = "\n".join(processed_my_playlist)

# ৩. সাধারণ প্লেলিস্ট লিঙ্কসমূহ
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
        "group_logo": "https://cdnhost.akashbd.net/assets/images/akash-facebook-banner.jpg?v=10.5.15",
        "url": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash-direct.m3u"
    },
    {
        "group_name": "BDIX TV",
        "group_logo": "https://bdix.net//wp-content/uploads/2019/04/bdxl-logo1.jpg",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/SM_bdix.m3u"
    },
    {
        "group_name": "RoarZone",
        "group_logo": "https://assets.appmeme.com/com.roarzone.tvapps--3-icon.png",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.m3u"
    },
    {
        "group_name": "BDIX",
        "group_logo": "https://cdn.aptoide.com/imgs/9/e/3/9e39cb70009f15ce7ec3203725a3ded8_icon.png",
        "url": "https://xtreamcode.allinonereborn.workers.dev/get.php?username=ratulhasanSa_246&password=1m43mozx&type=m3u_plus"
    },
    {
        "group_name": "AlixBD",
        "group_logo": "https://static.vecteezy.com/system/resources/thumbnails/007/688/855/small/tv-logo-free-vector.jpg",
        "url": "http://alixbd.com/2022.m3u"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

all_external_channels = []

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
            line_str = re.sub(r'group-title="[^"]*"', '', line_str)
            line_str = re.sub(r'tvg-group="[^"]*"', '', line_str)
            line_str = re.sub(r'group-title=\S+', '', line_str)
            line_str = re.sub(r'group-logo="[^"]*"', '', line_str)

            logo_attr = f' group-logo="{group_logo}"' if group_logo else ''
            
            if ',' in line_str:
                parts = line_str.split(',', 1)
                line_str = f'{parts[0].strip()} group-title="{group_name}"{logo_attr},{parts[1]}'
            else:
                line_str = f'{line_str} group-title="{group_name}"{logo_attr}'

        all_external_channels.append(line_str)


# ৪. STALKER PORTAL (HINDI, KIDS, BEN 10) ফিল্টার করে মূল প্লেলিস্টে যুক্ত করা
PORTAL_URL = "https://alex.rocktv.be/stalker_portal/c/"
MAC_ADDR = "00:1A:79:8C:0E:A7"
DEVICE_ID = "C4B0C9CA57DE7DAF4676BEEA9205402B11DD69C447496326F2CEC69AD1997460"
SERIAL_NUM = "B96257E7F728E"

stalker_headers = {
    'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stalkerphp/2.0.0 Safari/533.3',
    'X-User-Agent': 'Model: MAG250; Link: WiFi',
    'Cookie': f'mac={MAC_ADDR}; stb_lang=en; timezone=Europe%2FLondon',
    'Referer': PORTAL_URL
}

session = requests.Session()

def api_call(action, extra_params=""):
    url = f"{PORTAL_URL}portal.php?type=itv&action={action}&{extra_params}"
    try:
        res = session.get(url, headers=stalker_headers, timeout=15)
        return res.json()
    except Exception as e:
        return None

hs_data = api_call("handshake")
if hs_data and 'js' in hs_data and 'token' in hs_data['js']:
    stalker_headers['Authorization'] = f"Bearer {hs_data['js']['token']}"

genres_data = api_call("get_genres")
target_genres = {}

if genres_data and 'js' in genres_data:
    for g in genres_data['js']:
        g_id = str(g.get('id'))
        g_title = str(g.get('title', '')).strip().upper()
        if ("HINDI" in g_title and "NEWS" not in g_title) or ("KIDS" in g_title):
            target_genres[g_id] = g_title

for g_id, g_title in target_genres.items():
    ch_data = api_call("get_ordered_list", f"genre={g_id}&force_ch_link_check=1")
    if ch_data and 'js' in ch_data and 'data' in ch_data['js']:
        for ch in ch_data['js']['data']:
            ch_name = ch.get('name', '').strip()
            ch_cmd = ch.get('cmd', '')
            name_upper = ch_name.upper()
            
            if "24/7" in g_title or "24/7" in name_upper:
                if not ("BEN 10" in name_upper or "BEN10" in name_upper):
                    continue

            if ch_cmd:
                stream_cmd = ch_cmd.replace('ffmpeg ', '').strip()
                play_url = f"{PORTAL_URL}cmd/{stream_cmd}"
                all_external_channels.append(f'#EXTINF:-1 group-title="{g_title}",{ch_name}')
                all_external_channels.append(play_url)

# ৫. ফাইনাল ফাইল তৈরি করা
external_content = "\n".join(all_external_channels)
final_content = f"{my_playlist_updated}\n\n{external_content}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Updated everything into playlist.m3u successfully!")
