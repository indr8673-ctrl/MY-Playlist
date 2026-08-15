import re
import requests

# ১. আপনার tv.m3u ফাইল পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    my_playlist = "#EXTM3U"

# ==========================================================
# আপনার নোটপ্যাড (tv.m3u) এর ক্যাটাগরিগুলোর লোগো এখানে একবার সেট করুন
# ==========================================================
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
    # প্রয়োজনমতো "ক্যাটাগরির নাম": "লোগোর লিংক", এভাবে আরও যোগ করতে পারবেন
}

# ২. আপনার tv.m3u ফাইলের ক্যাটাগরিতে অটোমেটিক লোগো বসানো
processed_my_playlist = []
for line in my_playlist.splitlines():
    line_str = line.strip()
    if line_str.startswith('#EXTINF'):
        # group-title খুঁজে বের করা
        match = re.search(r'group-title="([^"]+)"', line_str)
        if match:
            group_name = match.group(1)
            # যদি এই গ্রুপের লোগো আমাদের লিস্টে থাকে
            if group_name in my_category_logos:
                logo_url = my_category_logos[group_name]
                # পুরনো group-logo বা tvg-logo মুছে নতুন লোগো বসানো
                line_str = re.sub(r'group-logo="[^"]*"', '', line_str)
                line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" group-logo="{logo_url}"')
                if 'tvg-logo=""' in line_str:
                    line_str = line_str.replace('tvg-logo=""', f'tvg-logo="{logo_url}"')
                elif 'tvg-logo="' not in line_str:
                    line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" tvg-logo="{logo_url}"')
    processed_my_playlist.append(line_str)

my_playlist_updated = "\n".join(processed_my_playlist)

# ৩. বাইরের অনলাইন প্লেলিস্ট যুক্ত করার অংশ
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
        "group_name": "Ayna TV",
        "group_logo": "https://aynaott.com/assets/images/logo/logo_bg.jpeg",
        "url": "https://raw.githubusercontent.com/abusaeeidx/Ayna-Playlists-free-Version/refs/heads/main/playlist.m3u"
    },
    {
        "group_name": "RoarZone",
        "group_logo": "https://assets.appmeme.com/com.roarzone.tvapps--3-icon.png",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.m3u"
    },
     {
        "group_name": "Voot",
        "group_logo": "https://play-lh.googleusercontent.com/InSOp5thAKQxms_ZZfRVjefSQFX2_WDTR1B03C3zcmxftJUkOWC2c__ciwfFLwxT2G6aRQmjfMV28-tnV6dE0w=w480-h960-rw",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/vood.m3u"
    },
    {
        "group_name": "Jio Hotstar",
        "group_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKe_1KwcBrLdVeWT8maozq2ukwcGBXFpxmlnTShnSCErmv5oAXbHVxqaW4&s=10",
        "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/jio_hotstar.m3u"
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

# ৪. ফাইল সেভ করা
external_content = "\n".join(all_external_channels)
final_content = f"{my_playlist_updated}\n\n{external_content}"

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("All Playlists and Categories updated with logos successfully!")

