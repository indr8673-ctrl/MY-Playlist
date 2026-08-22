import re
import requests

# ১. tv.m3u ফাইল পড়া
try:
    with open('tv.m3u', 'r', encoding='utf-8') as f:
        my_playlist = f.read().strip()
except Exception as e:
    print(f"Error reading tv.m3u: {e}")
    my_playlist = "#EXTM3U"

# ==========================================================
# আপনার সব ক্যাটাগরির লোগোর সম্পূর্ণ তালিকা
# ==========================================================
my_category_logos = {
    "Doraemon Season 08": "https://static.episodate.com/images/tv-show/full/73723.jpg",
    "Doraemon S08": "https://static.episodate.com/images/tv-show/full/73723.jpg",
    "Doraemon Season 09": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTi2q4-7myJaBDZh504ZzeIS2acbn4WvFXzxMbIJKnraA&s=10",
    "Doraemon Season 22": "https://images.justwatch.com/poster/339817061/s166/season-22.jpg",
    "Doraemon Season 20": "https://i.ytimg.com/vi/mFDyVwLIsyo/sddefault.jpg",
    "Doraemon Season 21": "https://image.tmdb.org/t/p/w500/al9BRFZuLzbuvhtrlTYs1ix1apu.jpg",
    "Doramon Movies": "https://image.tmdb.org/t/p/w500/al9BRFZuLzbuvhtrlTYs1ix1apu.jpg",
    "Doraemon": "https://image.tmdb.org/t/p/w500/al9BRFZuLzbuvhtrlTYs1ix1apu.jpg",
    "Avengers Movies": "https://spoilertown.com/wp-content/uploads/2024/06/avengers-age-of-ultron-2015.webp",
    "Avengers": "https://spoilertown.com/wp-content/uploads/2024/06/avengers-age-of-ultron-2015.webp",
    "Ben 10: Ultimate Alien [Hindi]": "https://i.ytimg.com/vi/Nle2PdBmlhQ/hq720.jpg",
    "Ben 10": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1V_Q6rLFMWvAiMy0HGJIxAB-isM5MK1iDOM0M9NoOecYUvgyg8DDR37eS&s=10",
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
    "Abox-Bdix": "https://pixeldrain.com/u/QHfF6CoF",
    "Music": "https://static.vecteezy.com/system/resources/previews/021/813/091/non_2x/music-tv-logo-design-template-with-tv-icon-and-music-icon-perfect-for-business-company-mobile-app-restaurant-etc-free-vector.jpg",
    "Toffee": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/DNMXs5UBm1RY_In7IJ72/posters/737b5c6e-8435-4cd8-81de-16a499fa6f4e.png"
}

# ২. tv.m3u প্রসেস করা
processed_my_playlist = []
for line in my_playlist.splitlines():
    line_str = line.strip()
    if line_str.startswith('#EXTINF'):
        match = re.search(r'group-title="([^"]+)"', line_str)
        if match:
            group_name = match.group(1)
            for key, logo_url in my_category_logos.items():
                if key.lower() in group_name.lower():
                    # tvg-logo এবং group-logo উভয় ক্ষেত্রেই সেট করা হচ্ছে
                    if 'tvg-logo=' not in line_str or 'tvg-logo=""' in line_str:
                        line_str = line_str.replace('#EXTINF:', f'#EXTINF: tvg-logo="{logo_url}" ')
                    if 'group-logo=' not in line_str or 'group-logo=""' in line_str:
                        line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" group-logo="{logo_url}"')
                    break
    processed_my_playlist.append(line_str)

my_playlist_updated = "\n".join(processed_my_playlist)

# ৩. বাইরের অনলাইন প্লেলিস্ট
playlists_to_add = [
    {"group_name": "Opplex TV", "group_logo": "https://e7.pngegg.com/pngimages/3/57/png-clipart-india-news-news-broadcasting-television-news-television-logo.png", "url": "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u", "indian_only": True},
    {"group_name": "Sony BD", "group_logo": "https://cdn.shortpixel.ai/spai/q_glossy+ret_img+to_webp/www.bizasialive.com/wp-content/uploads/2020/05/899ec721-sonylivnew001.jpg", "url": "http://140.245.107.220:5001/channels?url=https://ranapk-playlist.site/SONYBD.php"},
    {"group_name": "Sony BD 2", "group_logo": "https://ottking.in/wp-content/uploads/2022/12/sony-logo-768x768.jpg", "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/sonyLiv.m3u"},
    {"group_name": "Toffee BD", "group_logo": "https://cdn.aptoide.com/imgs/d/e/c/dec7398ec8030c41f581dab8c64a7876_fgraphic.jpg", "url": "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/refs/heads/main/toffee_playlist.m3u"},
    {"group_name": "AKASH", "group_logo": "https://cdnhost.akashbd.net/assets/images/akash-facebook-banner.jpg?v=10.5.15", "url": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"},
    {"group_name": "AKASH 2", "group_logo": "https://cdnhost.akashbd.net/assets/images/akash-facebook-banner.jpg?v=10.5.15", "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/akash_all_player.m3u"},
    {"group_name": "BDIX TV", "group_logo": "https://bdix.net//wp-content/uploads/2019/04/bdxl-logo1.jpg", "url": "https://xtreamcode.allinonereborn.workers.dev/playlist/8423f929.m3u"},
    {"group_name": "Ayna TV", "group_logo": "https://aynaott.com/assets/images/logo/logo_bg.jpeg", "url": "https://raw.githubusercontent.com/abusaeeidx/Ayna-BDIX-IPTV-Playlist/refs/heads/main/ayna-playlist.m3u"},
    {"group_name": "RoarZone", "group_logo": "https://assets.appmeme.com/com.roarzone.tvapps--3-icon.png", "url": "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.m3u"},
    {"group_name": "BDIX", "group_logo": "https://cdn.aptoide.com/imgs/9/e/3/9e39cb70009f15ce7ec3203725a3ded8_icon.png", "url": "https://xtreamcode.allinonereborn.workers.dev/get.php?username=ratulhasan5a_246&password=lm43mozx&type=m3u_plus"},
    {"group_name": "BDIX 2", "group_logo": "https://cdn.aptoide.com/imgs/9/e/3/9e39cb70009f15ce7ec3203725a3ded8_icon.png", "url": "https://raw.githubusercontent.com/mdabi0011-lab/Md-Abi-TV/refs/heads/main/mdabitv.m3u"},
    {"group_name": "Airtle", "group_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJgSPglUdjjlHBf0xYp1gN8OCmo4Qh3O7wrfvPozLkvqVKpXyEqe2-Zf03&s=10", "url": "http://140.245.107.220:5001/channels?url=https://ranapk-playlist.site/Darktv.php"},
    {"group_name": "DISH TV", "group_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyGvSp-6mhLM2r2dKmECZY6s0CdjlDbbO_ZHhRFKr3JV7kB8n-nVjaFfA&s=10", "url": "http://140.245.107.220:5001/channels?url=https://alex4528.site/playlist/dishtv.m3u"},
    {"group_name": "WATCHO", "group_logo": "https://img.utdstc.com/icon/6b0/3c7/6b03c798381482dfe5aa03b26b2431be6d7e6fcc00d14f27939ab525887d1fb9:600", "url": "http://140.245.107.220:5001/channels?url=https://gist.githubusercontent.com/ArcReactorCode/9ff3a4356291e6267ac76e30e4c44bc4/raw/watcho.m3u"},
    {"group_name": "AlixBD", "group_logo": "https://static.vecteezy.com/system/resources/thumbnails/007/688/855/small/tv-logo-free-vector.jpg", "url": "http://alixbd.com/2022.m3u"},
    {"group_name": "Voot", "group_logo": "https://play-lh.googleusercontent.com/InSOp5thAKQxms_ZZfRVjefSQFX2_WDTR1B03C3zcmxftJUkOWC2c__ciwfFLwxT2G6aRQmjfMV28-tnV6dE0w=w480-h960-rw", "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/vood.m3u"},
    {"group_name": "Jio TV", "group_logo": "https://crystalpng.com/wp-content/uploads/2025/10/jiotv-logo.png", "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/jio_tv.m3u"},
    {"group_name": "Jio Hotstar", "group_logo": "https://pbs.twimg.com/media/GjsHOY6WwAAAErg.jpg", "url": "https://raw.githubusercontent.com/sm-monirulislam/SM-IPTV/refs/heads/main/jio_hotstar.m3u"}
]

headers = {'User-Agent': 'Mozilla/5.0'}
all_external_channels = []

for item in playlists_to_add:
    group_name = item["group_name"]
    group_logo = item.get("group_logo", "")
    url = item["url"]
    indian_only = item.get("indian_only", False)

    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            lines = response.text.splitlines()
            skip_block = False
            
            for line in lines:
                line_str = line.strip()
                if not line_str or line_str.startswith('#EXTM3U'):
                    continue

                if line_str.startswith('#EXTINF'):
                    # Opplex TV-এর ফিল্টারিং
                    if indian_only:
                        is_indian = bool(re.search(r'group-title="[^"]*(IND|INDIAN)', line_str, re.I)) or "IND |" in line_str or "INDIAN |" in line_str
                        if not is_indian:
                            skip_block = True
                            continue
                        else:
                            skip_block = False
                    else:
                        skip_block = False

                    # গ্রুপ আপডেট
                    if 'group-title="' in line_str:
                        line_str = re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', line_str)
                    else:
                        parts = line_str.split(',', 1)
                        if len(parts) == 2:
                            line_str = f'{parts[0].strip()} group-title="{group_name}",{parts[1]}'

                    # যদি চ্যানেলের নিজস্ব tvg-logo না থাকে, তবে ডিফল্ট গ্রুপের লোগো যোগ করা
                    if group_logo:
                        if 'tvg-logo="' not in line_str or 'tvg-logo=""' in line_str:
                            line_str = line_str.replace('#EXTINF:', f'#EXTINF: tvg-logo="{group_logo}" ')
                        if 'group-logo="' not in line_str or 'group-logo=""' in line_str:
                            line_str = line_str.replace(f'group-title="{group_name}"', f'group-title="{group_name}" group-logo="{group_logo}"')

                    all_external_channels.append(line_str)
                
                elif not skip_block:
                    all_external_channels.append(line_str)

    except Exception:
        continue

# ৪. আউটপুট ফাইল তৈরি
external_content = "\n".join(all_external_channels)
final_content = f"{my_playlist_updated}\n\n{external_content}" if external_content else my_playlist_updated

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Playlist successfully updated with fixed logos!")
