import re
import requests

# আপনার ফিল্টার করা সার্ভারের M3U URL (এখানে আপনার লিংক বসাবেন)
PROVIDER_M3U_URL = "https://xtreamcode.allinonereborn.workers.dev/get.php?username=ratulhasanSa_246&password=1m43mozx&type=m3u_plus"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

filtered_channels = ["#EXTM3U"]

try:
    response = requests.get(PROVIDER_M3U_URL, headers=headers, timeout=30)
    if response.status_code == 200:
        lines = response.text.splitlines()
        include_next = False
        
        for i in range(len(lines)):
            line = lines[i].strip()
            
            if line.startswith('#EXTINF'):
                # গ্রুপ টাইটেল ম্যাচ করা
                group_match = re.search(r'group-title="([^"]+)"', line)
                group_name = group_match.group(1).upper() if group_match else ""
                
                # ১. হিন্দি সেকশন
                is_hindi = "HINDI" in group_name and "NEWS" not in group_name
                
                # ২. কিডস সেকশন
                is_kids = group_name == "KIDS"
                
                # ৩. KIDS 24/7 থেকে শুধু বেন টেন (Ben 10)
                is_ben10 = "24/7" in group_name and ("BEN 10" in line.upper() or "BEN10" in line.upper())
                
                if is_hindi or is_kids or is_ben10:
                    include_next = True
                    filtered_channels.append(line)
                else:
                    include_next = False
                    
            elif include_next and line and not line.startswith('#'):
                filtered_channels.append(line)
                include_next = False

except Exception as e:
    print(f"Error fetching provider: {e}")

# ফিল্টার করা চ্যানেলগুলো আলাদা ফাইলে সেভ হবে
with open('filtered_channels.m3u', 'w', encoding='utf-8') as f:
    f.write("\n".join(filtered_channels))

print("নতুন ফিল্টার করা প্লেলিস্ট তৈরি হয়ে গেছে!")
