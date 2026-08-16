import os

ben10_m3u = "ben_10_alien_force.m3u"
playlist_file = "playlist.m3u"

# ফাইল দুটি সত্যি আছে কি না যাচাই করে কাজ করা
if os.path.exists(playlist_file) and os.path.exists(ben10_m3u):
    try:
        with open(ben10_m3u, "r", encoding="utf-8") as f:
            ben10_lines = f.readlines()
        
        clean_lines = [line for line in ben10_lines if not line.startswith("#EXTM3U")]
        
        if clean_lines:
            with open(playlist_file, "a", encoding="utf-8") as f:
                f.write("\n" + "".join(clean_lines))
            print("Ben 10 Alien Force added successfully!")
    except Exception as e:
        print(f"Error merging files: {e}")
else:
    print("Required files not found, skipping merge.")
