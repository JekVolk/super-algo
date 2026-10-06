import urllib.request, re

urls = [
    "https://ucpc.eolymp.space/",
    "https://ucpc.eolymp.space/uk/compete",
    "https://ucpc.eolymp.space/uk/compete/ucpc2026practice",
    "https://ucpc.eolymp.space/uk/problems",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', text)
            print(f"URL: {url} -> {resp.status} Title: {title.group(1) if title else 'No title'} Length: {len(text)}")
    except Exception as e:
        print(f"URL: {url} -> Error {e}")
