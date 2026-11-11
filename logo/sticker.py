"""Logo ales (câinele cu pălărie în fața soarelui) + 6 variante de palmier, cu textură de desen.
python3 logo/sticker.py  ->  logo/sticker/P1.svg ... P6.svg + index.html"""
from pathlib import Path

OUT = Path(__file__).parent / "sticker"
OUT.mkdir(exist_ok=True)
CREAM, FOREST, OLIVE, GOLD = "#f6eddb", "#1b2b18", "#8fa83a", "#e9a93b"

# ---------- câinele (exact ca varianta aleasă) ----------
HEAD = ("M60 30 C74 30 84 38 85 50 C86 60 82 68 76 74 C72 80 67 86 60 86 "
        "C53 86 48 80 44 74 C38 68 34 60 35 50 C36 38 46 30 60 30 Z")
EARS = ("M80 37 C93 37 99 50 97 66 C96 75 89 77 86 71 C84 63 83 52 80 37 Z "
        "M40 37 C27 37 21 50 23 66 C24 75 31 77 34 71 C36 63 37 52 40 37 Z")
BLAZE = ("M60 37 C63 37 64.5 44 64.5 51 C71 55 75 62 75 70 C75 79 68 85 60 85 "
         "C52 85 45 79 45 70 C45 62 49 55 55.5 51 C55.5 44 57 37 60 37 Z")
NOSE = "M53.5 63.5 C53.5 60 66.5 60 66.5 63.5 C66.5 67.5 62.5 70 60 70 C57.5 70 53.5 67.5 53.5 63.5 Z"
SMILE = "M51.5 73 C55.5 77.5 64.5 77.5 68.5 73"
CHEST = "M46 81 C35 87 29 99 27 116 L93 116 C91 99 85 87 74 81 C70 86 50 86 46 81 Z"
HAT_CROWN = "M42 34 C42 22 50 15.5 60 15.5 C70 15.5 78 22 78 34 Z"
HAT_BAND = "M42.4 28 C50 31.5 70 31.5 77.6 28 L78 33.5 C70 36.5 50 36.5 42 33.5 Z"
HAT_BRIM = "M28 36.5 C34 30 86 30 92 36.5 C86 42 34 42 28 36.5 Z"


def dog():
    return (f'<g transform="translate(60 116) scale(.86) translate(-60 -116)">'
            f'<path d="{CHEST}" fill="{FOREST}"/>'
            f'<path d="{EARS}" fill="{FOREST}" stroke="{CREAM}" stroke-width="2"/>'
            f'<path d="{HEAD}" fill="{FOREST}"/><path d="{BLAZE}" fill="{CREAM}"/><path d="{NOSE}" fill="{FOREST}"/>'
            f'<path d="M60 70 V73.5" stroke="{FOREST}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<path d="{SMILE}" fill="none" stroke="{FOREST}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<circle cx="49" cy="52" r="3" fill="{CREAM}"/><circle cx="71" cy="52" r="3" fill="{CREAM}"/>'
            f'<path d="{HAT_BRIM}" fill="{CREAM}"/><path d="{HAT_CROWN}" fill="{CREAM}"/><path d="{HAT_BAND}" fill="{OLIVE}"/>'
            f'</g>')


SUN = f'<circle cx="60" cy="66" r="48" fill="{GOLD}"/>'

# ---------- frunze ----------
# zimțată (cea din varianta aleasă)
FROND = "M0 0 C14 -15 40 -18 62 2 L54 0 L56 6 L46 -2 L47 4 L37 -3 L37 3 L27 -3 L26 2 L17 -2 L15 1 Z"
# lungă, căzută, cu vârful arcuit (pentru palmier „pletos”)
FROND_LONG = ("M0 0 C18 -16 50 -18 74 8 L66 3 L67 10 L57 1 L57 7 L47 -2 L46 4 L36 -3 L35 2 "
              "L25 -3 L23 1.5 L14 -2 L12 1 Z")
# frunză simplă, rotunjită (fără zimți) — pentru logo-ul final
FROND_ROUND = "M0 0 C9 -11 32 -15 53 -7 C60 -4 61 2 56 4 C37 2.5 17 3 0 0 Z"
WHITE = "#ffffff"


def outlined(art, w=3.2):
    """Contur alb în jurul siluetei: aceeași grafică, desenată dedesubt cu tușă albă groasă."""
    halo = (art.replace(f'fill="{OLIVE}"', f'fill="{WHITE}"').replace(f'fill="{FOREST}"', f'fill="{WHITE}"')
            .replace(f'stroke="{CREAM}"', f'stroke="{WHITE}"'))
    return (f'<g stroke="{WHITE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round">{halo}</g>' + art)


# frunză netedă, cu nervură (stil desenat)
FROND_SOFT = "M0 0 C16 -14 44 -15 64 4 C46 -2 22 -2 0 0 Z"


def crown(sc, fill, kind=FROND, rots=((-8, .62), (-42, .56), (-8, .62, 1), (-42, .56, 1), (-82, .46)), rib=None):
    out = f'<g fill="{fill}">'
    for r in rots:
        rot, s = r[0], r[1]
        mir = len(r) > 2
        tr = f'{"scale(-1 1) " if mir else ""}rotate({rot}) scale({s * sc:.3f})'
        out += f'<path d="{kind}" transform="{tr}"/>'
        if rib:
            out += (f'<path d="M3 -.5 C20 -9 42 -9 60 2" fill="none" stroke="{rib}" stroke-width="1.6" '
                    f'stroke-linecap="round" transform="{tr}"/>')
    return out + "</g>"


def nuts(sc, fill):
    return (f'<g fill="{fill}"><circle cx="{-3 * sc:.2f}" cy="{4 * sc:.2f}" r="{3.2 * sc:.2f}"/>'
            f'<circle cx="{3 * sc:.2f}" cy="{5 * sc:.2f}" r="{3.2 * sc:.2f}"/></g>')


def trunk(x, y, tx, ty, w, fill, bend=0.0, rings=None):
    """Trunchi conic de la (x,y) la (tx,ty); bend > 0 îl curbează spre dreapta la mijloc."""
    mx, my = (x + tx) / 2 + bend, (y + ty) / 2
    d = (f"M{x - w / 2} {y} Q{mx - w * .42} {my} {tx - w * .32} {ty} "
         f"L{tx + w * .32} {ty} Q{mx + w * .42} {my} {x + w / 2} {y} Z")
    out = f'<path d="{d}" fill="{fill}"/>'
    if rings:
        for i in range(1, 9):
            t = i / 9.5
            # punct pe curba centrală (Bezier quadratic)
            px = (1 - t) ** 2 * x + 2 * (1 - t) * t * mx + t ** 2 * tx
            py = (1 - t) ** 2 * y + 2 * (1 - t) * t * my + t ** 2 * ty
            ww = w * (1 - .35 * t) * .5
            out += (f'<path d="M{px - ww:.1f} {py:.1f} q{ww:.1f} {-2.2:.1f} {2 * ww:.1f} 0" fill="none" '
                    f'stroke="{rings}" stroke-width="1.1" stroke-linecap="round"/>')
    return out


# ---------- cele 6 palmieri ----------
P = {}
# 1. Clasic (cel din varianta aleasă)
P["P1"] = ("Clasic", trunk(96, 112, 90, 26, 6, OLIVE) +
           f'<g transform="translate(90 26)">{crown(.78, OLIVE)}{nuts(.78, FOREST)}</g>')
# 2. Curbat, aplecat spre dreapta, cu inele pe trunchi
ROUND_ROTS = ((-4, .62), (-38, .58), (-74, .5), (-6, .6, 1), (-40, .56, 1))
_t2 = trunk(88, 114, 95, 30, 8, OLIVE, bend=-7, rings=CREAM)
_trunk2, _rings2 = _t2.split("/>", 1)[0] + "/>", _t2.split("/>", 1)[1]
P["P2"] = ("Curbat cu inele", outlined(_trunk2 +
           f'<g transform="translate(95 30) rotate(6)">{crown(.74, OLIVE, FROND_ROUND, ROUND_ROTS)}{nuts(.78, FOREST)}</g>')
           + _rings2)
# 3. Doi palmieri: unul mare în dreapta, unul mic în stânga
P["P3"] = ("Doi palmieri", trunk(96, 112, 92, 22, 6, OLIVE, bend=-3) +
           f'<g transform="translate(92 22) rotate(6)">{crown(.78, OLIVE)}{nuts(.78, FOREST)}</g>' +
           trunk(24, 100, 30, 44, 4.5, OLIVE, bend=3) +
           f'<g transform="translate(30 44) rotate(-8)">{crown(.52, OLIVE)}{nuts(.52, FOREST)}</g>')
# 4. Pletos: frunze lungi care cad, coroană bogată
P["P4"] = ("Pletos", trunk(94, 114, 96, 24, 7, OLIVE, bend=-5, rings=CREAM) +
           f'<g transform="translate(96 24) rotate(4)">' +
           crown(.66, OLIVE, FROND_LONG, ((8, .62), (-24, .6), (-56, .5), (-88, .42), (-20, .58, 1), (12, .6, 1), (40, .5))) +
           nuts(.8, FOREST) + "</g>")
# 5. Două tonuri: trunchi verde închis, frunze oliv, coroana mare peste soare
P["P5"] = ("Două tonuri", trunk(97, 114, 88, 22, 7, FOREST, bend=-2, rings=OLIVE) +
           f'<g transform="translate(88 22)">{crown(.92, OLIVE)}{nuts(.92, GOLD)}</g>')
# 6. Desenat: frunze netede cu nervură, trunchi subțire
P["P6"] = ("Frunze cu nervură", trunk(92, 114, 94, 26, 5.5, OLIVE, bend=-4) +
           f'<g transform="translate(94 26) rotate(6)">' +
           crown(.85, OLIVE, FROND_SOFT, ((6, .6), (-28, .58), (-62, .5), (-94, .4), (-26, .56, 1), (8, .56, 1), (40, .46)), rib=CREAM) +
           nuts(.85, FOREST) + "</g>")

# ---------- textură „desenat de mână” ----------
TEXTURE = """<filter id="hand" x="-4%" y="-4%" width="108%" height="108%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="4" result="wob"/>
  <feDisplacementMap in="SourceGraphic" in2="wob" scale="2.4" xChannelSelector="R" yChannelSelector="G" result="rough"/>
  <feTurbulence type="fractalNoise" baseFrequency="2.4" numOctaves="2" seed="11" result="grain"/>
  <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -16 12.2" result="speckle"/>
  <feComposite in="rough" in2="speckle" operator="in" result="ink"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.25" numOctaves="2" seed="2" result="tone"/>
  <feColorMatrix in="tone" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .3 -.13" result="shade"/>
  <feComposite in="shade" in2="ink" operator="in" result="shadeIn"/>
  <feMerge><feMergeNode in="ink"/><feMergeNode in="shadeIn"/></feMerge>
</filter>"""


def svg(palm, textured=True, bg=None):
    f = ' filter="url(#hand)"' if textured else ""
    bgr = f'<rect x="-10" y="-10" width="140" height="140" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -6 130 130" width="1200" height="1200">'
            f'<defs>{TEXTURE}</defs>{bgr}<g{f}>{SUN}{palm}{dog()}</g></svg>\n')


cards = []
for k, (name, palm) in P.items():
    (OUT / f"{k}.svg").write_text(svg(palm))
    (OUT / f"{k}-fara-textura.svg").write_text(svg(palm, False))
    (OUT / f"{k}-crem.svg").write_text(svg(palm, False, CREAM))   # sursă pentru textura din Photoshop
    cards.append(f'<figure><img src="{k}.svg" alt="{name}"><figcaption><b>{k[1]}</b> {name}</figcaption></figure>')

(OUT / "index.html").write_text(f"""<!doctype html><html lang="ro"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Pet Holiday – variante palmier</title>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Nunito:wght@600;800&display=swap" rel="stylesheet">
<style>
body {{ margin: 0; background: {CREAM}; font-family: Nunito, sans-serif; color: {FOREST}; }}
h1 {{ font: 700 36px Oswald, sans-serif; text-transform: uppercase; margin: 0; padding: 36px 24px 4px; text-align: center; }}
p {{ text-align: center; margin: 0 0 10px; color: #5d6556; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; padding: 20px 24px 50px; max-width: 1200px; margin: 0 auto; }}
figure {{ margin: 0; background: #fbf6ea; border-radius: 22px; padding: 18px; box-shadow: 0 16px 34px -26px rgba(0,0,0,.45); }}
img {{ width: 100%; display: block; }}
figcaption {{ text-align: center; font-weight: 800; margin-top: 6px; }}
figcaption b {{ color: {OLIVE}; margin-right: 6px; }}
</style></head><body>
<h1>Variante de palmier</h1><p>Același câine, 6 palmieri diferiți, cu textură de desen (margini ușor tremurate și granulație).</p>
<div class="grid">{''.join(cards)}</div></body></html>""")
print("ok")
