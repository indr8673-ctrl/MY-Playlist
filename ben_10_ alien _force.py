import os

ben10_m3u = "ben_10_alien_force.m3u"
playlist_file = "playlist.m3u"

# update.py দিয়ে তৈরি হওয়া playlist.m3u ফাইলের নিচে বেন টেন যুক্ত করা
if os.path.exists(playlist_file) and os.path.exists(ben10_m3u):
    with open(ben10_m3u, "r", encoding="utf-8") as f:
        ben10_lines = f.readlines()
    
    # #EXTM3U বাদ দিয়ে শুধু লিংকগুলো নিয়ে প্লেলিস্টের নিচে জুড়ে দেওয়া
    clean_lines = [line for line in ben10_lines if not line.startswith("#EXTM3U")]
    
    with open(playlist_file, "a", encoding="utf-8") as f:
        f.write("\n" + "".join(clean_lines))

    print("Ben 10 Alien Force added to playlist.m3u successfully!")
