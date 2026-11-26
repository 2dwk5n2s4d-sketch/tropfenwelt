# Tropfenwelt

Interaktive 3D-Welt der Fischgärtnerei für das Touch-Display (Planar) im Hofladen.

## Dateien

| Datei | Zweck |
|---|---|
| `fischgaertnerei-tropfenwelt.html` | Das ganze Spiel in einer Datei: Startbild, Erklärung, 1–4 Spieler nebeneinander |
| `setup.py` | Einmalig am Home Assistant: holt 3D-Bibliothek und Schriften in den Ordner |
| `update.py` | Stündlich am Home Assistant: holt die neueste Fassung aus diesem Repository |

## Betrieb

Die Dateien liegen am Home Assistant unter `/config/www/tropfenwelt/` und sind
im Netz erreichbar unter `http://<home-assistant>/local/tropfenwelt.html`.

Eine neue Fassung wird hier abgelegt; der Home Assistant holt sie stündlich und
der Planar lädt sie nach, sobald er am Startbild steht. Ein laufendes Spiel wird
nicht unterbrochen.
