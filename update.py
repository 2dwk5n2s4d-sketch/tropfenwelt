#!/usr/bin/env python3
"""Holt die neueste Tropfenwelt aus dem GitHub-Repository in den Ordner www/tropfenwelt.
Laeuft stuendlich ueber eine Home-Assistant-Automation. Wird nur ersetzt, wenn die
heruntergeladene Datei vollstaendig und neu ist."""
import hashlib, os, sys, urllib.request

RAW = "https://raw.githubusercontent.com/2dwk5n2s4d-sketch/tropfenwelt/main/"
ZIEL = "/config/www/tropfenwelt/"
DATEIEN = ["fischgaertnerei-tropfenwelt.html", "update.py"]
MIN = {"fischgaertnerei-tropfenwelt.html": 1_000_000, "update.py": 500}

def hole(name):
    req = urllib.request.Request(RAW + name, headers={"User-Agent": "tropfenwelt-update"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def main():
    os.makedirs(ZIEL, exist_ok=True)
    geaendert = []
    for name in DATEIEN:
        try:
            neu = hole(name)
        except Exception as e:
            print("Fehler beim Laden von", name, e); continue
        if len(neu) < MIN.get(name, 1):
            print("zu klein, uebersprungen:", name, len(neu)); continue
        if name.endswith(".html") and not neu.lstrip().startswith(b"<!DOCTYPE"):
            print("kein HTML, uebersprungen:", name); continue
        pfad = ZIEL + name
        alt = open(pfad, "rb").read() if os.path.exists(pfad) else b""
        if hashlib.md5(alt).hexdigest() == hashlib.md5(neu).hexdigest():
            continue
        tmp = pfad + ".neu"
        with open(tmp, "wb") as f:
            f.write(neu)
        os.replace(tmp, pfad)
        geaendert.append(name)
    print("aktualisiert:", geaendert if geaendert else "nichts")

if __name__ == "__main__":
    sys.exit(main())
