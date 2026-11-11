"""6 direcții noi de palmier pentru logo-ul ales (frunze rotunjite + contur alb).
python3 logo/palmieri.py  ->  logo/palmieri/Q1.svg ... Q6.svg"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sticker import (CREAM, FOREST, OLIVE, GOLD, SUN, dog, trunk, nuts, outlined, TEXTURE)  # noqa: E402

OUT = Path(__file__).parent / "palmieri"
OUT.mkdir(exist_ok=True)

# frunze rotunjite: dreaptă și căzută (vârful coboară)
LEAF = "M0 0 C9 -11 32 -15 53 -7 C60 -4 61 2 56 4 C37 2.5 17 3 0 0 Z"
LEAF_DROOP = "M0 0 C12 -13 36 -15 54 -1 C60 4 59 10 53 9 C40 1 20 2 0 0 Z"
LEAF_FAT = "M0 0 C8 -14 30 -20 50 -10 C60 -5 61 5 53 7 C36 5 16 5 0 0 Z"


def fan(leaf, sc, fill, rots):
    out = f'<g fill="{fill}">'
    for r in rots:
        rot, s = r[0], r[1]
        mir = len(r) > 2
        out += f'<path d="{leaf}" transform="{"scale(-1 1) " if mir else ""}rotate({rot}) scale({s * sc:.3f})"/>'
    return out + "</g>"


def split_rings(t):
    a, b = t.split("/>", 1)
    return a + "/>", b


Q = {}

# 1. Drept, coroană bogată (7 frunze) — clasic, echilibrat
t, r = split_rings(trunk(94, 114, 92, 26, 7.5, OLIVE, bend=-2, rings=CREAM))
Q["Q1"] = ("Drept, coroană bogată", outlined(t + '<g transform="translate(92 26)">' + fan(LEAF, .7, OLIVE, (
    (-2, .62), (-34, .6), (-66, .52), (-96, .42), (-4, .6, 1), (-36, .56, 1), (24, .46))) + nuts(.75, FOREST) + "</g>") + r)

# 2. Aplecat peste câine: coroana deasupra pălăriei
t, r = split_rings(trunk(98, 114, 78, 24, 7.5, OLIVE, bend=10, rings=CREAM))
Q["Q2"] = ("Aplecat peste câine", outlined(t + '<g transform="translate(78 24) rotate(-14)">' + fan(LEAF, .68, OLIVE, (
    (0, .62), (-36, .56), (-72, .46), (-2, .6, 1), (-36, .54, 1), (26, .44, 1))) + nuts(.72, FOREST) + "</g>") + r)

# 3. Două tonuri: trunchi verde închis, frunze oliv, mai scurt
t, r = split_rings(trunk(96, 114, 92, 34, 8, FOREST, bend=-3, rings=OLIVE))
Q["Q3"] = ("Două tonuri", outlined(t + '<g transform="translate(92 34)">' + fan(LEAF, .72, OLIVE, (
    (-2, .62), (-38, .58), (-74, .48), (-4, .6, 1), (-38, .54, 1))) + nuts(.75, GOLD) + "</g>") + r)

# 4. Doar frunze care ies din spatele soarelui (fără trunchi)
Q["Q4"] = ("Doar frunze, din spatele soarelui", outlined(
    '<g transform="translate(94 42)">' + fan(LEAF, .7, OLIVE, ((-8, .62), (-40, .6), (-74, .52), (-104, .44), (20, .5))) + "</g>"
    + '<g transform="translate(26 46)">' + fan(LEAF, .56, OLIVE, ((-8, .6, 1), (-42, .56, 1), (-76, .46, 1))) + "</g>", 3.4), True)

# 5. Fântână: frunze lungi care cad în arc
t, r = split_rings(trunk(95, 114, 92, 26, 7, OLIVE, bend=-4, rings=CREAM))
Q["Q5"] = ("Frunze căzute (fântână)", outlined(t + '<g transform="translate(92 26)">' + fan(LEAF_DROOP, .68, OLIVE, (
    (6, .6), (-26, .56), (-62, .48), (-92, .38), (4, .58, 1), (-28, .52, 1), (38, .48), (40, .44, 1))) + nuts(.72, FOREST) + "</g>") + r)

# 6. Pitic, cartoon: trunchi gros și scurt, frunze grase
t, r = split_rings(trunk(94, 114, 90, 52, 12, OLIVE, bend=-3, rings=CREAM))
Q["Q6"] = ("Pitic, cartoon", outlined(t + '<g transform="translate(90 52)">' + fan(LEAF_FAT, .7, OLIVE, (
    (-4, .6), (-40, .56), (-80, .46), (-6, .58, 1), (-42, .52, 1))) + nuts(.95, FOREST) + "</g>") + r)


def svg(palm, behind_sun=False, bg=CREAM):
    body = (palm + SUN) if behind_sun else (SUN + palm)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -6 130 130" width="1200" height="1200">'
            f'<rect x="-10" y="-10" width="140" height="140" fill="{bg}"/>{body}{dog()}</svg>\n')


for k, v in Q.items():
    name, palm = v[0], v[1]
    behind = len(v) > 2 and v[2]
    (OUT / f"{k}.svg").write_text(svg(palm, behind))
print("ok")
