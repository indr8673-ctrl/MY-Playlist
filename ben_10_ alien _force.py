import os

playlist_file = "playlist.m3u"
ben10_m3u = "ben_10_alien_force.m3u"

# ১. ben_10_alien_force.m3u ফাইলের কনটেন্ট পড়া
ben10_content = ""
if os.path.exists(ben10_m3u):
    with open(ben10_m3u, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # #EXTM3U বাদ দিয়ে চ্যানেলগুলো আলাদা করা
        clean_lines = [line for line in lines if not line.startswith("#EXTM3U")]
        ben10_content = "".join(clean_lines)

# ২. মূল playlist.m3u ফাইলটি পড়ে তার শেষে কার্টুনগুলো সরাসরি যুক্ত করা
if os.path.exists(playlist_file) and ben10_content:
    with open(playlist_file, "r", encoding="utf-8") as f:
        current_playlist = f.read()

    # আগের প্লেলিস্টের নিচে বেন টেনের এপিসোডগুলো যুক্ত করা
    updated_playlist = current_playlist.strip() + "\n" + ben10_content.strip()

    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write(updated_playlist)

    print("Ben 10 Alien Force channels merged successfully!")
else:
    print("Playlist or Ben 10 file not found.")
