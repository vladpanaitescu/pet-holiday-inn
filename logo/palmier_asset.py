"""Palmierul dat de client (SVG/Asset 1.svg) pus pe logo: trunchiul ascuns în spatele câinelui,
3 poziționări, contur alb. python3 logo/palmier_asset.py  ->  logo/palmier-asset/A.svg, B.svg, C.svg"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from sticker import CREAM, OLIVE, SUN, dog  # noqa: E402

OUT = ROOT / "palmier-asset"
OUT.mkdir(exist_ok=True)
SRC = (ROOT.parent / "SVG" / "Asset 1.svg").read_text()
PALM_D = re.search(r'<path d="([^"]+)"', SRC).group(1)
JX, JY = 643, 490          # punctul din care pleacă frunzele, în coordonatele fișierului (1287×1436)
WHITE = "#ffffff"


def palm(x, y, s, mirror=False, rot=0, outline=1.9, color=WHITE):
    """Pune joncțiunea coroanei în (x,y), la scara s; outline = grosimea conturului alb în unități de logo."""
    sx = -s if mirror else s
    tr = f"translate({x} {y}) rotate({rot}) scale({sx} {s}) translate({-JX} {-JY})"
    return (f'<g transform="{tr}">'
            f'<path d="{PALM_D}" fill="{color}" stroke="{color}" stroke-width="{2 * outline / s:.0f}" stroke-linejoin="round"/>'
            f'<path d="{PALM_D}" fill="{OLIVE}"/></g>')


V = {
    "A": ("Dreapta sus", palm(87, 30, .045, rot=8)),
    "B": ("Centrat, deasupra pălăriei", palm(60, 25, .046)),
    "C": ("Stânga sus", palm(33, 30, .045, mirror=True, rot=-8)),
    # varianta finală: poziția și mărimea din macheta clientului, contur crem ca la urechi
    "F": ("Final", palm(86.6, 29.7, .055, rot=16, outline=1.72, color=CREAM)),
}


def svg(p, bg=CREAM):
    bgr = f'<rect x="-10" y="-10" width="140" height="140" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -6 130 130" width="1200" height="1200">'
            f'{bgr}{SUN}{p}{dog()}</svg>\n')


# variantă cu contur crem și pe soare și pe pieptul câinelui (ca la urechi)
from sticker import CHEST, FOREST  # noqa: E402
SUN_STROKE = SUN.replace("/>", f' stroke="{CREAM}" stroke-width="1.72"/>')
DOG_STROKE = dog().replace(f'<path d="{CHEST}" fill="{FOREST}"/>',
                           f'<path d="{CHEST}" fill="{FOREST}" stroke="{CREAM}" stroke-width="2" stroke-linejoin="round"/>')


def svg_stroke(p, bg=CREAM):
    bgr = f'<rect x="-10" y="-10" width="140" height="140" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -6 130 130" width="1200" height="1200">'
            f'{bgr}{SUN_STROKE}{p}{DOG_STROKE}</svg>\n')


(OUT / "G.svg").write_text(svg_stroke(V["F"][1]))
(OUT / "G-transparent.svg").write_text(svg_stroke(V["F"][1], None))
(OUT / "G-verde.svg").write_text(svg_stroke(V["F"][1], "#1b2b18"))
(OUT / "F-verde.svg").write_text(svg(V["F"][1], "#1b2b18"))

# gradiente subtile (mai puțin flat): înlocuim doar umplerile, conturul și liniile rămân pline
GRADS = """<defs>
<radialGradient id="gSun" cx=".36" cy=".3" r=".85"><stop offset="0" stop-color="#f5c46a"/><stop offset=".55" stop-color="#e9a93b"/><stop offset="1" stop-color="#d48f2a"/></radialGradient>
<linearGradient id="gForest" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b4227"/><stop offset=".5" stop-color="#1b2b18"/><stop offset="1" stop-color="#121d10"/></linearGradient>
<linearGradient id="gOlive" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#a6c04f"/><stop offset=".6" stop-color="#8fa83a"/><stop offset="1" stop-color="#748c2b"/></linearGradient>
<linearGradient id="gCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fcf7ec"/><stop offset=".6" stop-color="#f6eddb"/><stop offset="1" stop-color="#e8d6b4"/></linearGradient>
</defs>"""


def gradient(svg_text):
    t = (svg_text.replace(f'fill="{GOLD}"', 'fill="url(#gSun)"').replace(f'fill="{FOREST}"', 'fill="url(#gForest)"')
         .replace(f'fill="{OLIVE}"', 'fill="url(#gOlive)"'))
    # crem: doar formele câinelui (bot, ochi, pălărie), nu fundalul și nu conturul palmierului
    body_start = t.index("<g transform=\"translate(60 116)")
    t = t[:body_start] + t[body_start:].replace(f'fill="{CREAM}"', 'fill="url(#gCream)"')
    i = t.index(">", t.index("<svg")) + 1
    return t[:i] + GRADS + t[i:]


from sticker import GOLD  # noqa: E402
for nm, bg in (("H", CREAM), ("H-transparent", None), ("H-verde", "#1b2b18")):
    (OUT / f"{nm}.svg").write_text(gradient(svg_stroke(V["F"][1], bg)))

for k, (name, p) in V.items():
    (OUT / f"{k}.svg").write_text(svg(p))
    (OUT / f"{k}-transparent.svg").write_text(svg(p, None))
print("ok")
