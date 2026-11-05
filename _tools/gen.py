"""Nano Banana Pro: python3 gen.py OUT.png AR "prompt" [img ...]  (cheia din docx-ul Gemini B2B, nu se afiseaza)"""
import base64, json, re, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path

KEY_DOCX = Path.home() / "Documents/ShopBGS/2026/septembrie/b2b/cheie-gemini.docx"
MODEL = "gemini-3-pro-image"


def key():
    txt = subprocess.run(["textutil", "-convert", "txt", "-stdout", str(KEY_DOCX)], capture_output=True, text=True).stdout
    return re.search(r"(AQ\.[A-Za-z0-9_.-]+|AIza[A-Za-z0-9_-]{30,})", txt).group(0)


out, ar, prompt, *imgs = sys.argv[1:]
parts = [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(Path(p).read_bytes()).decode()}} for p in imgs]
parts.append({"text": prompt})
body = {"contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ar, "imageSize": "2K"}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key()})
for attempt in range(4):
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            res = json.loads(r.read()); break
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:400]
        if e.code in (429, 500, 502, 503, 504) and attempt < 3:
            time.sleep(30 * (attempt + 1)); continue
        sys.exit(f"FAIL {out} HTTP {e.code} {msg}")
for c in res.get("candidates", []):
    for p in c.get("content", {}).get("parts", []):
        d = p.get("inlineData") or p.get("inline_data")
        if d:
            Path(out).write_bytes(base64.b64decode(d["data"])); print("OK", out); sys.exit()
sys.exit(f"FAIL {out} fara imagine: {json.dumps(res)[:300]}")
