import os

# ১. বেন টেনের m3u ফাইলের নাম এবং মূল প্লেলিস্ট ফাইলের নাম
ben10_m3u_file = "ben_10_alien_force.m3u"
playlist_file = "playlist.m3u"

# ২. ben_10_alien_force.m3u ফাইল থেকে লিঙ্ক এনে playlist.m3u-তে যুক্ত করা
if os.path.exists(ben10_m3u_file) and os.path.exists(playlist_file):
    with open(ben10_m3u_file, "r", encoding="utf-8") as f:
        ben10_lines = f.readlines()
    
    # #EXTM3U লাইন বাদ দিয়ে শুধু ভিডিও লিঙ্ক ও টাইটেল নেওয়া
    clean_lines = [line for line in ben10_lines if not line.startswith("#EXTM3U")]
    
    # playlist.m3u ফাইলের নিচে সব এপিসোড যুক্ত করা
    with open(playlist_file, "a", encoding="utf-8") as f:
        f.write("\n" + "".join(clean_lines))

    print("Ben 10 Alien Force episodes added to playlist.m3u successfully!")
else:
    print("Error: Files not found for merging.")
