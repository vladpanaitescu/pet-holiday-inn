"""Scoate fiecare variantă din logo/index.html ca SVG de sine stătător (fără <use>), fără fundal, în două seturi de culori (pentru fundal deschis / închis).
Folosire: python3 logo/export.py  ->  logo/svg/L1-deschis.svg ... L6-inchis.svg"""
import re
from pathlib import Path

HERE = Path(__file__).parent
html = (HERE / "index.html").read_text()
defs = html[html.index("  <defs>") + 8: html.index("  </defs>")]

C = {"forest": "#1b2b18", "olive": "#8fa83a", "gold": "#e9a93b", "cream": "#f6eddb"}
THEMES = {
    "deschis": dict(c0=C["cream"], c1=C["forest"], c2=C["olive"], c3=C["gold"]),   # pentru fundal deschis
    "inchis": dict(c0=C["forest"], c1=C["cream"], c2=C["gold"], c3=C["gold"]),     # pentru fundal închis
}

# forme de bază (path-uri cu id) și simboluri
paths = {m.group(1): m.group(2) for m in re.finditer(r'<path id="([\w-]+)" d="([^"]+)"/>', defs)}
symbols = {m.group(1): m.group(2) for m in re.finditer(r'<symbol id="(L\d)" viewBox="0 0 120 120">(.*?)</symbol>', defs, re.S)}


def inline_uses(body):
    # <use href="#x" attrs.../>  ->  <path d="..." attrs.../>
    def rep(m):
        ref, attrs = m.group(1), m.group(2)
        return f'<path d="{paths[ref]}"{attrs}/>'
    return re.sub(r'<use href="#([\w-]+)"([^/]*)/>', rep, body)


out = HERE / "svg"
out.mkdir(exist_ok=True)
for sid, body in symbols.items():
    body = inline_uses(body)
    for name, t in THEMES.items():
        b = body
        for k, v in t.items():
            b = b.replace(f"var(--{k})", v)
        (out / f"{sid}-{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="1200" height="1200">{b}</svg>\n')
print("ok", len(symbols))
