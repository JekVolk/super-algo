import urllib.request

url = "https://ucpc.eolymp.space/uk/compete/ucpc2026practice/problem/4"
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    }
)
try:
    with urllib.request.urlopen(req) as resp:
        print("Status:", resp.status)
        data = resp.read()
        print("Headers:", resp.headers)
        # Check if gzip
        if resp.headers.get('Content-Encoding') == 'gzip':
            import gzip
            data = gzip.decompress(data)
        elif resp.headers.get('Content-Encoding') == 'br':
            import brotli
            data = brotli.decompress(data)
        text = data.decode('utf-8', errors='ignore')
        print("Length:", len(text))
        with open("scratch/direct_fetch.html", "w", encoding="utf-8") as f:
            f.write(text)
        print("Saved to scratch/direct_fetch.html")
except Exception as e:
    print("Error:", e)
