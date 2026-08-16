import os

playlist_file = "playlist.m3u"
ben10_m3u = "ben_10_alien_force.m3u"

# ১. M3U ফাইল থেকে ডাটা পড়া
ben10_content = ""
if os.path.exists(ben10_m3u):
    with open(ben10_m3u, "r", encoding="utf-8") as f:
        lines = f.readlines()
        clean_lines = [line for line in lines if not line.startswith("#EXTM3U")]
        ben10_content = "".join(clean_lines)

# ২. playlist.m3u ফাইলে যুক্ত করা
if os.path.exists(playlist_file) and ben10_content:
    with open(playlist_file, "r", encoding="utf-8") as f:
        current_data = f.read()

    # আগের সব চ্যানেলের ঠিক নিচে নতুন এপিসোডগুলো পেস্ট করা
    updated_data = current_data.strip() + "\n\n" + ben10_content.strip()

    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write(updated_data)

    print("SUCCESS: Ben 10 episodes added to playlist.m3u")
else:
    print("ERROR: File not found or empty!")
