import os

playlist_file = "playlist.m3u"
ben10_m3u = "ben_10_alien_force.m3u"

# ১. বেন টেন ফাইলের নাম খোঁজা (স্পেস বা ছোট/বড় হাতের অক্ষরের সমস্য দূর করতে)
matched_ben10_file = None
if os.path.exists(ben10_m3u):
    matched_ben10_file = ben10_m3u
else:
    for file in os.listdir('.'):
        if "ben_10" in file.lower() and file.endswith(".m3u"):
            matched_ben10_file = file
            break

if matched_ben10_file:
    # ২. বেন টেন ফাইলের ডেটা পড়া
    with open(matched_ben10_file, "r", encoding="utf-8") as f:
        ben10_lines = f.readlines()
    
    clean_ben10_content = "".join([line for line in ben10_lines if not line.startswith("#EXTM3U")])

    # ৩. playlist.m3u ফাইলে জোড়া লাগানো
    if os.path.exists(playlist_file):
        with open(playlist_file, "r", encoding="utf-8") as f:
            main_playlist_data = f.read()

        updated_playlist = main_playlist_data.strip() + "\n\n" + clean_ben10_content.strip()

        with open(playlist_file, "w", encoding="utf-8") as f:
            f.write(updated_playlist)

        print("Ben 10 channels added successfully!")
else:
    print("Ben 10 M3U file not found!")
