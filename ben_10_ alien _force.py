import os

playlist_file = "playlist.m3u"
ben10_m3u = "ben_10_alien_force.m3u"

def merge_playlists():
    # বেন টেন ফাইলটি খোঁজা (স্পেস বা নাম যাই থাক)
    matched_ben10_file = None
    if os.path.exists(ben10_m3u):
        matched_ben10_file = ben10_m3u
    else:
        for file in os.listdir('.'):
            if "ben_10" in file.lower() and file.endswith(".m3u"):
                matched_ben10_file = file
                break

    if not matched_ben10_file:
        print("Error: Ben 10 M3U file not found!")
        return

    # ১. বেন টেন ফাইলের কন্টেন্ট পড়া (#EXTM3U বাদ দিয়ে)
    with open(matched_ben10_file, "r", encoding="utf-8") as f:
        ben10_lines = f.readlines()
    
    clean_ben10_content = "".join([line for line in ben10_lines if not line.startswith("#EXTM3U")])

    # ২. মূল playlist.m3u ফাইলের সাথে জোড়া লাগানো
    if os.path.exists(playlist_file):
        with open(playlist_file, "r", encoding="utf-8") as f:
            main_playlist_data = f.read()

        # প্লেলিস্টের মূল ডাটার নিচে বেন টেন যুক্ত করা
        updated_playlist = main_playlist_data.strip() + "\n\n" + clean_ben10_content.strip()

        with open(playlist_file, "w", encoding="utf-8") as f:
            f.write(updated_playlist)

        print("SUCCESS: Ben 10 Alien Force channels appended successfully to playlist.m3u!")
    else:
        print("Error: playlist.m3u file does not exist!")

if __name__ == "__main__":
    merge_playlists()
