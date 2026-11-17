"""Pregătește site-ul pentru urcare pe Hostico: copiază doar fișierele folosite în dist/
și face arhiva dist/petholidayinn.zip (se extrage în public_html).
python3 _tools/pachet.py"""
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE = ROOT / "dist" / "site"
PAGES = ["index.html", "regulament.html", "termeni.html", "confidentialitate.html"]
ALWAYS = ["styles.css", "main.js", "contact.php", ".htaccess", "assets/fonts.css"]

files = set(PAGES + ALWAYS)
# tot ce e legat din pagini și CSS (imagini, fonturi), fără parametrul ?v=
for f in PAGES + ["styles.css", "assets/fonts.css"]:
    text = (ROOT / f).read_text()
    base = Path(f).parent
    for ref in re.findall(r'(?:src|href|srcset)="([^"#]+)"|url\(["\']?([^"\')]+)', text):
        ref = next(r for r in ref if r).split("?")[0]
        if ref.startswith(("http", "mailto:", "tel:", "data:", "//")) or not ref:
            continue
        p = (base / ref).as_posix()
        if (ROOT / p).is_file():
            files.add(p)

if SITE.exists():
    shutil.rmtree(SITE)
for f in sorted(files):
    dst = SITE / f
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / f, dst)

zip_path = DIST / "petholidayinn.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SITE.rglob("*")):
        if p.is_file():
            z.write(p, p.relative_to(SITE).as_posix())

size = sum(p.stat().st_size for p in SITE.rglob("*") if p.is_file())
print(f"{len(files)} fișiere, {size / 1e6:.1f} MB -> {zip_path.relative_to(ROOT)} ({zip_path.stat().st_size / 1e6:.1f} MB)")
for f in sorted(files):
    print("  ", f)
