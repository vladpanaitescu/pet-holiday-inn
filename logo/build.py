"""Construiește logo/index.html (6 variante: câinele din față, ușor întors spre stânga, palmier aplecat spre dreapta).
Fără cercuri sau fundaluri colorate. Rulează apoi logo/export.py pentru SVG-urile separate."""
from pathlib import Path

HERE = Path(__file__).parent

# ---------- forme de bază (viewBox 120) ----------
# Capul e întors ușor spre stânga: botul și ochii se mută spre stânga,
# urechea din spate (stânga) e mai îngustă, cea din față (dreapta) mai lată.
HEAD = ("M57 30 C72 30 84 38 85.5 50 C87 61 82 69 75 75 C70 81 64 86 56 86 "
        "C49 86 44 81 41 75 C37 68 35 60 36.5 50 C38 38 46 30 57 30 Z")
EARS_DOWN = ("M79 36 C93 36 100 50 98 67 C97 76 89 78 86 72 C84 63 83 52 79 36 Z "
             "M42 37 C33 38 28.5 50 30 63 C31 71 35 72 37.5 67.5 C39 60 39.5 51 42 37 Z")
EARS_UP = "M71 33 L87 10 C93 23 93 37 86 48 Z M44 34 L35 13 C31 24 32 37 38 47 Z"
BLAZE = ("M54 37 C57 37 58.5 44 58.5 51 C65 55 69 62 69 70 C69 79 62 85 54 85 "
         "C46.5 85 40.5 79 40.5 70 C40.5 62 44 55 49.5 51 C49.5 44 51 37 54 37 Z")
NOSE = "M47 63.5 C47 60 60 60 60 63.5 C60 67.5 56 70 53.5 70 C51 70 47 67.5 47 63.5 Z"
TONGUE = "M49.3 75.5 C49.3 85 57.7 85 57.7 75.5 Z"
SMILE = "M45 73 C49 77.5 58 77.5 62 73"
EYES = ((44, 51.5, 2.6), (66, 52, 3.1))
CHEST = "M46 81 C35 87 29 99 27 116 L93 116 C91 99 85 87 74 81 C70 86 50 86 46 81 Z"
HAT_CROWN = "M42 34 C42 22 50 15.5 60 15.5 C70 15.5 78 22 78 34 Z"
HAT_BAND = "M42.4 28 C50 31.5 70 31.5 77.6 28 L78 33.5 C70 36.5 50 36.5 42 33.5 Z"
HAT_BRIM = "M28 36.5 C34 30 86 30 92 36.5 C86 42 34 42 28 36.5 Z"
HAT_T = "translate(-2.5 1) rotate(-8 60 34)"
FROND = "M0 0 C14 -15 40 -18 62 2 L54 0 L56 6 L46 -2 L47 4 L37 -3 L37 3 L27 -3 L26 2 L17 -2 L15 1 Z"


def crown(sc, fill, nuts="none"):
    f = lambda rot, s, mirror=False: (f'<use href="#frond" transform="{"scale(-1 1) " if mirror else ""}'
                                      f'rotate({rot}) scale({s * sc:.3f})"/>')
    out = (f'<g fill="{fill}">' + f(-8, .62) + f(-42, .56) + f(-8, .62, True) + f(-42, .56, True)
           + f(-82, .46) + "</g>")
    if nuts != "none":
        out += (f'<g fill="{nuts}"><circle cx="{-3 * sc:.2f}" cy="{4 * sc:.2f}" r="{3.2 * sc:.2f}"/>'
                f'<circle cx="{3 * sc:.2f}" cy="{5 * sc:.2f}" r="{3.2 * sc:.2f}"/></g>')
    return out


def palm(x, y, top_dx, h, sc, fill, nuts="none", w=5, tilt=14):
    """Trunchi de la (x,y) care se apleacă spre dreapta cu top_dx; coroana înclinată cu `tilt` grade."""
    tx, ty = x + top_dx, y - h
    # curbură: pleacă aproape vertical și se apleacă spre vârf
    trunk = (f'<path d="M{x - w / 2} {y} C{x - w / 2} {y - h * .45} {tx - w * .4 - top_dx * .25} {y - h * .8} {tx - w * .35} {ty} '
             f'L{tx + w * .35} {ty} C{tx + w * .25 - top_dx * .25} {y - h * .8} {x + w / 2} {y - h * .45} {x + w / 2} {y} Z" '
             f'fill="{fill}"/>')
    return trunk + f'<g transform="translate({tx} {ty}) rotate({tilt})">{crown(sc, fill, nuts)}</g>'


DOG_T = "translate(57 116) scale(.86) translate(-60 -116)"


def dog(c_body, c_cut, c_hat, c_band, c_tongue, hat=True, collar=None, chest=True, t=DOG_T):
    out = f'<g transform="{t}">'
    if chest:
        out += f'<use href="#chest" fill="{c_body}"/>'
    if hat:
        out += f'<use href="#earsDown" fill="{c_body}" stroke="{c_cut}" stroke-width="2"/>'
    else:
        out += f'<use href="#earsUp" fill="{c_body}"/>'
    out += f'<use href="#head" fill="{c_body}"/><use href="#blaze" fill="{c_cut}"/><use href="#nose" fill="{c_body}"/>'
    out += f'<path d="M53.5 70 V73.5" stroke="{c_body}" stroke-width="1.8" stroke-linecap="round"/>'
    out += f'<use href="#tongue" fill="{c_tongue}"/>'
    out += f'<path d="{SMILE}" fill="none" stroke="{c_body}" stroke-width="1.8" stroke-linecap="round"/>'
    out += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c_cut}"/>' for x, y, r in EYES)
    if collar:
        out += (f'<path d="M46 85 C53 90.5 64 90.5 71 85" fill="none" stroke="{collar}" stroke-width="3.6" stroke-linecap="round"/>'
                f'<circle cx="57" cy="94" r="4" fill="{collar}"/>')
    if hat:
        out += (f'<g transform="{HAT_T}"><use href="#hatBrim" fill="{c_hat}"/><use href="#hatCrown" fill="{c_hat}"/>'
                f'<use href="#hatBand" fill="{c_band}"/></g>')
    return out + '</g>'


# ---------- cele 6 variante (fără fundal) ----------
P = dict(x=71, y=114, top_dx=20, h=84)          # palmierul: pornește din spatele umărului, se apleacă spre dreapta
V = {}

# 1. Color: pălărie aurie, palmier oliv, zgardă aurie
V["L1"] = (palm(**P, sc=.66, fill="var(--c2)", nuts="var(--c3)", w=8)
           + dog("var(--c1)", "var(--c0)", "var(--c3)", "var(--c2)", "var(--c3)", True, "var(--c3)"))

# 2. Silueta: o singură culoare
V["L2"] = (palm(**P, sc=.66, fill="var(--c1)", nuts="var(--c1)", w=8)
           + dog("var(--c1)", "var(--c0)", "var(--c1)", "var(--c0)", "var(--c0)", True, None))

# 3. Două culori: totul verde închis, doar pălăria aurie
V["L3"] = (palm(**P, sc=.66, fill="var(--c1)", nuts="var(--c3)", w=8)
           + dog("var(--c1)", "var(--c0)", "var(--c3)", "var(--c1)", "var(--c3)", True, "var(--c3)"))

# 4. Urechi sus: fără pălărie
V["L4"] = (palm(**P, sc=.68, fill="var(--c2)", nuts="var(--c1)", w=8)
           + dog("var(--c1)", "var(--c0)", "", "", "var(--c3)", False, "var(--c3)"))

# 5. Linie
V["L5"] = (
    '<g fill="none" stroke="var(--c1)" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">'
    + palm(**P, sc=.66, fill="none", w=6.5)
    + f'<g transform="{DOG_T}">'
    + '<use href="#chest" fill="var(--c0)"/><use href="#earsDown" fill="var(--c0)"/><use href="#head" fill="var(--c0)"/>'
    + '<use href="#blaze"/><use href="#nose" fill="var(--c1)"/>'
    + f'<path d="M53.5 70 V73.5"/><path d="{SMILE}"/><use href="#tongue" fill="var(--c3)"/>'
    + '<path d="M46 85 C53 90.5 64 90.5 71 85"/><circle cx="57" cy="94" r="3.4" fill="var(--c3)"/>'
    + f'<g transform="{HAT_T}"><use href="#hatBrim" fill="var(--c0)"/><use href="#hatCrown" fill="var(--c0)"/>'
    + '<path d="M42.4 29 C50 32.5 70 32.5 77.6 29"/></g>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r - .3}" fill="var(--c1)" stroke="none"/>' for x, y, r in EYES)
    + '</g></g>')

# 6. Doar capul: mai mare, pentru avatar / favicon
V["L6"] = (palm(68, 104, 18, 76, .64, "var(--c2)", "var(--c3)", 8)
           + dog("var(--c1)", "var(--c0)", "var(--c3)", "var(--c2)", "var(--c3)", True, None, False,
                 "translate(57 104) scale(1.12) translate(-60 -86)"))

NAMES = [
    ("Color", "Câinele cu pălăria de pai, ușor întors spre stânga, cu palmierul aplecat spre dreapta în spate. Varianta principală."),
    ("Silueta", "O singură culoare, siluetă plină. Merge pe broderie, ștampilă, gravură, zgardă."),
    ("Două culori", "Totul verde închis, doar pălăria și zgarda aurii. Sobru, dar tot jucăuș."),
    ("Urechi sus", "Fără pălărie: câinele cu urechile ciulite, palmierul oliv aplecat în spatele lui."),
    ("Linie", "Desen liniar, curat. Bun pentru semnalistică și materiale tipărite."),
    ("Doar capul", "Capul mare cu pălăria și palmierul — pentru avatar de Instagram și favicon."),
]

DEFS = f'''<path id="head" d="{HEAD}"/>
    <path id="earsDown" d="{EARS_DOWN}"/>
    <path id="earsUp" d="{EARS_UP}"/>
    <path id="blaze" d="{BLAZE}"/>
    <path id="nose" d="{NOSE}"/>
    <path id="tongue" d="{TONGUE}"/>
    <path id="chest" d="{CHEST}"/>
    <path id="hatCrown" d="{HAT_CROWN}"/>
    <path id="hatBand" d="{HAT_BAND}"/>
    <path id="hatBrim" d="{HAT_BRIM}"/>
    <path id="frond" d="{FROND}"/>'''

symbols = "\n".join(f'    <symbol id="{k}" viewBox="0 0 120 120">{v}</symbol>' for k, v in V.items())

html = (HERE / "index.html").read_text()
a, b = html.index("  <defs>"), html.index("  </defs>") + len("  </defs>")
html = html[:a] + f"  <defs>\n    {DEFS}\n{symbols}\n  </defs>" + html[b:]
a, b = html.index("  const items = ["), html.index("  ];") + len("  ];")
html = html[:a] + "  const items = [\n" + ",\n".join(f'    ["{n}", "{d}"]' for n, d in NAMES) + "\n  ];" + html[b:]
(HERE / "index.html").write_text(html)
print("ok")
