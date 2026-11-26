#!/usr/bin/env python3
"""Einmalig am Home Assistant ausfuehren: holt 3D-Bibliothek und Schriften in den
Ordner www/tropfenwelt, damit der Planar ohne Internet auskommt."""
import os, re, urllib.request

ZIEL = "/config/www/tropfenwelt/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
LIBS = {
    "three.min.js": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
    "OrbitControls.js": "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js",
}
CSS = ("https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700"
       "&family=Playfair+Display:wght@700&display=swap")

def lade(url, kopf=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers=kopf or {}), timeout=120) as r:
        return r.read()

def main():
    os.makedirs(ZIEL, exist_ok=True)
    for name, url in LIBS.items():
        if os.path.exists(ZIEL + name) and os.path.getsize(ZIEL + name) > 10000:
            print("vorhanden:", name); continue
        open(ZIEL + name, "wb").write(lade(url))
        print("geladen:", name)
    # Schriften: CSS holen, Schriftdateien daneben legen, Pfade auf lokal umschreiben
    css = lade(CSS, UA).decode()
    for i, url in enumerate(sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)))):
        name = "font%02d.woff2" % i
        if not os.path.exists(ZIEL + name):
            open(ZIEL + name, "wb").write(lade(url, UA))
        css = css.replace(url, name)
    open(ZIEL + "fonts.css", "w").write(css)
    print("Schriften fertig:", len(re.findall(r"font\d+\.woff2", css)), "Dateien")

if __name__ == "__main__":
    main()
