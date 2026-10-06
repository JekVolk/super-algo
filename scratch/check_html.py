with open("scratch/direct_fetch.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
print("Matches for 'ucpc':", len(re.findall(r'ucpc', text, re.I)))
print("Matches for 'problem':", len(re.findall(r'problem', text, re.I)))
print("Matches for '4':", len(re.findall(r'4', text)))

# Let's search for next.js state or JSON
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
print("Number of scripts:", len(scripts))
for i, s in enumerate(scripts):
    if len(s) > 100:
        print(f"Script {i} len {len(s)}: {s[:200]}")
