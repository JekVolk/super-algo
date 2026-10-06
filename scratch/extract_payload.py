with open("scratch/direct_fetch.html", "r", encoding="utf-8") as f:
    text = f.read()

import re, json

pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', text)
full_payload = "".join(pushes).replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n')

with open("scratch/payload.txt", "w", encoding="utf-8") as f:
    f.write(full_payload)

print("Saved payload.txt, length:", len(full_payload))

# Search for statements, titles, markdown, problem descriptions
for pattern in [r'"statement":\{.*?\}', r'"title":"(.*?)"', r'"name":"(.*?)"', r'ucpc2026practice']:
    matches = re.findall(pattern, full_payload)
    print(f"Matches for {pattern}: {len(matches)}")
    if matches and pattern != r'"name":"(.*?)"':
        print("  Sample:", matches[:5])
