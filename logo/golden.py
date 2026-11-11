"""Logo Pet Holiday: golden retriever în stil negative-space + palmier aplecat spre dreapta.
python3 logo/golden.py  ->  logo/golden/golden-*.svg"""
from pathlib import Path

OUT = Path(__file__).parent / "golden"
OUT.mkdir(exist_ok=True)
INK, PAPER = "#2f2f2f", "#ffffff"

# ---------- câinele (privește spre stânga; botul în stânga) ----------
# partea apropiată: craniu + urechea mare, cu marginea ușor ondulată (blană de golden)
NEAR = ("M106 44 C122 38 143 42 153 56 C160 66 161 80 157 93 "
        "C164 104 168 116 167 128 C170 132 168 137 165 139 C166 146 161 152 154 154 "
        "C150 158 143 157 140 152 C135 154 130 150 130 144 C129 138 129 132 129 127 "
        "C128 126 126 120 121 115 C118 112 115 110 112 109 "
        "C114 96 113 82 109 70 C107 62 106 52 106 44 Z")
# partea depărtată: petic pe frunte (în jurul ochiului din spate)
FAR = ("M96 45 C82 46 70 54 64 66 C60 74 60 82 62 88 C68 89 74 87 79 83 "
       "C86 77 91 69 94 60 C95.5 54 96 49 96 45 Z")
# urechea din spate, care se vede pe sub obraz
FAR_EAR = ("M54 121 C46 128 40 141 41 154 C41 160 44 164 48 166 C53 169 59 166 62 160 "
           "C64 152 63 142 61 133 C60 128 58 124 54 121 Z")
# pieptul pufos de golden, sub bărbie (margine jos ondulată)
RUFF = ("M60 140 C72 156 94 165 120 163 C128 162 134 160 138 156 C137 168 131 178 121 184 "
        "C117 179 110 178 105 182 C100 177 93 177 88 181 C84 175 77 174 72 177 C70 165 66 152 60 140 Z")
NOSE = "M42 99 C41 91 61 88 66 96 C70 103 63 112 56 115 C49 113 43 107 42 99 Z"
NOSE_HI = "M48 95 C52 92 58 92 61 94"
# gura zâmbitoare (linie groasă) + limba
SMILE = "M56 115 C58 125 66 131 77 129 C84 128 90 123 94 117"
TONGUE = "M67 128 C65 138 70 146 77 145 C83 144 85 137 83 129 C78 131 72 131 67 128 Z"
TONGUE_LINE = "M75 132 L75.5 141"
# ochi: semilună veselă (arc) + punct de lumină
EYE_NEAR = "M106 80 C109 85 117 85 120 79"
EYE_FAR = "M70 75 C72 80 79 80 82 75"

# ---------- palmierul (în spate, aplecat spre dreapta) ----------
TRUNK = ("M134 214 C137 178 146 142 157 110 C163 92 168 74 173 58 "
         "L183 61 C178 78 173 96 168 114 C158 146 152 180 151 214 Z")
FROND = "M0 0 C14 -15 40 -18 62 2 L55 0 L57 5.5 L47 -2 L48 3.5 L38 -3 L38 2.5 L28 -3 L27 1.5 L18 -2 L16 1 Z"
FRONDS = [  # (unghi, scară, oglindit)
    (8, 1.7, False), (-24, 1.65, False), (-58, 1.35, False), (-92, 1.0, False),
    (-28, 1.55, True), (2, 1.45, True), (40, 1.1, False),
]


def palm(tx=178, ty=58):
    """Coroana la (tx,ty), trunchiul pleacă de jos din spatele câinelui."""
    out = f'<path d="{TRUNK}" fill="{INK}"/>'
    out += "".join(f'<path d="M{a} {b} q4 -2 9 0" fill="none" stroke="{PAPER}" stroke-width="1.8" stroke-linecap="round" transform="rotate(-18 {a} {b})"/>'
                   for a, b in [(150, 180), (153, 160), (157, 140), (162, 121), (167, 103), (172, 86)])
    out += f'<g transform="translate({tx} {ty})">'
    for ang, sc, mir in FRONDS:
        tr = f'{"scale(-1 1) " if mir else ""}rotate({ang}) scale({sc})'
        out += f'<path d="{FROND}" fill="{INK}" transform="{tr}"/>'
    out += f'<circle cx="-3" cy="5" r="5" fill="{INK}"/><circle cx="5" cy="6" r="5" fill="{INK}"/></g>'
    return out


def dog(gap=4.5):
    # contur alb în jurul formelor câinelui, ca să se despartă de palmier
    shapes = [NEAR, FAR, NOSE, TONGUE, RUFF]
    halo = "".join(f'<path d="{d}" fill="{PAPER}" stroke="{PAPER}" stroke-width="{gap*2}" stroke-linejoin="round"/>' for d in shapes)
    # zona albă a feței/pieptului ca să acopere palmierul în spatele capului
    face = ('<path d="M96 44 C100 40 104 40 106 44 C110 70 114 96 112 109 C120 116 128 128 128 150 '
            'C128 170 118 190 100 196 C80 196 64 186 60 166 C58 150 56 136 54 121 C48 116 42 108 42 99 '
            'C44 92 52 88 62 88 C60 74 70 54 96 44 Z" fill="' + PAPER + '"/>')
    ink = (f'<path d="{NEAR}" fill="{INK}"/><path d="{FAR}" fill="{INK}"/><path d="{RUFF}" fill="{INK}"/>'
           f'<path d="{NOSE}" fill="{INK}"/>'
           f'<path d="{NOSE_HI}" fill="none" stroke="{PAPER}" stroke-width="2.6" stroke-linecap="round"/>'
           f'<path d="{SMILE}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
           f'<path d="{TONGUE}" fill="{INK}"/>'
           f'<path d="{TONGUE_LINE}" stroke="{PAPER}" stroke-width="2" stroke-linecap="round"/>'
           f'<path d="{EYE_NEAR}" fill="none" stroke="{PAPER}" stroke-width="3.4" stroke-linecap="round"/>'
           f'<path d="{EYE_FAR}" fill="none" stroke="{PAPER}" stroke-width="3" stroke-linecap="round"/>')
    return halo + face + ink


def svg(body, *_):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="34 -16 272 272" width="1000" height="1000">{body}</svg>\n'


# variante: golurile sunt transparente (mască), deci logo-ul merge peste orice fundal
VB = "34 -16 272 272"
INK, PAPER = "#fff", "#000"          # în mască: alb = vizibil, negru = gol
mask_body = palm() + dog()


def masked(color, bg=None):
    rect_bg = f'<rect x="34" y="-16" width="272" height="272" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" width="1000" height="1000">'
            f'<defs><mask id="m" maskUnits="userSpaceOnUse" x="34" y="-16" width="272" height="272">'
            f'<rect x="34" y="-16" width="272" height="272" fill="#000"/>'
            f'<g transform="translate(10 10)">{mask_body}</g></mask></defs>'
            f'{rect_bg}<rect x="34" y="-16" width="272" height="272" fill="{color}" mask="url(#m)"/></svg>\n')


for name, color in {"verde": "#1b2b18", "negru": "#2f2f2f", "crem": "#f6eddb", "auriu": "#e9a93b"}.items():
    (OUT / f"golden-{name}.svg").write_text(masked(color))
# previzualizări cu fundal
(OUT / "_preview-crem.svg").write_text(masked("#1b2b18", "#f6eddb"))
(OUT / "_preview-verde.svg").write_text(masked("#f6eddb", "#1b2b18"))
print("ok")
