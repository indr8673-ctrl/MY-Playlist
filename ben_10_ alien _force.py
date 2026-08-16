import os

playlist_file = "playlist.m3u"

# ১. বেন টেন M3U ফাইলটি খুঁজে বের করা
ben10_file_path = None
for file in os.listdir('.'):
    if "ben" in file.lower() and file.endswith(".m3u"):
        ben10_file_path = file
        break

if ben10_file_path:
    print(f"Found Ben 10 file: {ben10_file_path}")
    
    # ২. বেন টেন ফাইলের ডেটা পড়া
    with open(ben10_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    clean_ben10 = "".join([line for line in lines if not line.startswith("#EXTM3U")])

    # ৩. playlist.m3u ফাইলের নিচে টেক্সট যুক্ত করা
    if os.path.exists(playlist_file):
        with open(playlist_file, "r", encoding="utf-8") as f:
            main_playlist = f.read()

        updated_playlist = main_playlist.strip() + "\n\n" + clean_ben10.strip()

        with open(playlist_file, "w", encoding="utf-8") as f:
            f.write(updated_playlist)

        print("SUCCESS: Ben 10 episodes merged into playlist.m3u successfully!")
    else:
        print("ERROR: playlist.m3u file not found.")
else:
    print("ERROR: Ben 10 M3U file not found in repository.")
