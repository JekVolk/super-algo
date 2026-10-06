path = r'C:\Users\JekVo\.gemini\antigravity-cli\brain\f2f34115-b25e-40e2-b5a0-060259bffdb3\.system_generated\steps\546\content.md'
with open(path, 'rb') as f:
    raw = f.read()

# Try different encodings
for enc in ['utf-8', 'cp1251', 'iso-8859-1']:
    try:
        s = raw.decode(enc)
        print(f"--- Decoded with {enc} ---")
        import re
        ua = [w for w in re.findall(r'[а-яА-ЯіІїЇєЄґҐ\w]{3,}', s) if any(c in 'іїєґІЇЄҐ' for c in w)]
        print(f"Ukrainian words sample ({len(ua)}):", ua[:10])
        break
    except Exception as e:
        print(enc, "failed:", e)
