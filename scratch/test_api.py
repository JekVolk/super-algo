import urllib.request, json

endpoints = [
    "https://api.eolymp.com/spaces/ucpc/contests",
    "https://api.eolymp.com/spaces/ucpc2026practice/contests",
    "https://api.eolymp.com/spaces/ucpc/contests/ucpc2026practice",
    "https://api.eolymp.com/contests/ucpc2026practice",
    "https://api.eolymp.com/spaces/ucpc2026practice",
    "https://api.eolymp.com/spaces/ucpc/problems",
]

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8')
            print(f"OK {ep} -> {data[:200]}")
    except Exception as e:
        print(f"FAIL {ep} -> {e}")
