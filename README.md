# Pet Holiday – site de prezentare

Site static (HTML/CSS/JS) + `contact.php` pentru formular. Animații cu GSAP + ScrollTrigger + Lenis (CDN).

Rulare locală: `python3 -m http.server 5178` și deschide http://localhost:5178
(local, fără PHP, formularul arată confirmarea ca demo).

## De completat înainte de lansare
- Telefon (+40 778 393 527), email (petholidayinn@gmail.com) și adresa (Str. Pârâului 5, Măgurele) sunt puse.
- **`FROM` din `contact.php`**: de schimbat pe o adresă de pe domeniul final (ex. no-reply@domeniu.ro) când avem domeniul.
- De confirmat cu clientul textele care nu vin din Instagram: secțiunile Servicii, Cum funcționează, FAQ, pisici.

## Imagini
- `_source/` – postările originale de pe Instagram (640 px).
- `_gen/` – scenele curățate de text cu Nano Banana Pro (`_tools/gen.py`); `vet`, `pisica`, `joaca` sunt generate în stilul locației.
- `assets/img/` – versiunile WebP folosite pe site.
