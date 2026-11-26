#!/usr/bin/env python3
"""Richtet am Home Assistant den Abgleich auf Befehl ein:
  - shell_command.tropfenwelt_update in configuration.yaml
  - Skript 'Tropfenwelt aktualisieren' in scripts.yaml (per Knopf ausloesbar, auch am Handy)
Entfernt eine frueher eingetragene stuendliche Automation wieder.
Legt vor jeder Aenderung Sicherungskopien an."""
import os, re, shutil

CONF = "/config/configuration.yaml"
AUTO = "/config/automations.yaml"
SCRI = "/config/scripts.yaml"
CMD = '  tropfenwelt_update: "python3 /config/www/tropfenwelt/update.py"'
SKRIPT = """
tropfenwelt_aktualisieren:
  alias: Tropfenwelt aktualisieren
  icon: mdi:cloud-download
  description: Holt die neueste Fassung des Spiels aus dem GitHub-Repository
  sequence:
    - action: shell_command.tropfenwelt_update
  mode: single
"""

def sichern(p, name):
    if os.path.exists(p) and not os.path.exists(p + ".bak-" + name):
        shutil.copy2(p, p + ".bak-" + name)

def conf():
    s = open(CONF).read() if os.path.exists(CONF) else ""
    if "tropfenwelt_update" in s:
        print("configuration.yaml: schon eingetragen"); return
    sichern(CONF, "tropfenwelt")
    m = re.search(r"^shell_command:[ \t]*$", s, re.M)
    s = (s[:m.end()] + "\n" + CMD + s[m.end():]) if m else (s.rstrip("\n") + "\n\nshell_command:\n" + CMD + "\n")
    open(CONF, "w").write(s)
    print("configuration.yaml: shell_command eingetragen")

def automation_weg():
    if not os.path.exists(AUTO):
        return
    s = open(AUTO).read()
    if "id: tropfenwelt_update" not in s:
        print("automations.yaml: keine stuendliche Automation vorhanden"); return
    sichern(AUTO, "tropfenwelt2")
    zeilen, raus, neu = s.split("\n"), False, []
    for z in zeilen:
        if z.startswith("- ") and "id: tropfenwelt_update" in z.replace("- ", "", 1):
            raus = True; continue
        if raus and z.startswith("- "):
            raus = False
        if not raus:
            neu.append(z)
    s = "\n".join(neu).strip("\n") + "\n"
    open(AUTO, "w").write(s if s.strip() else "[]\n")
    print("automations.yaml: stuendliche Automation entfernt")

def skript():
    s = open(SCRI).read() if os.path.exists(SCRI) else ""
    if "tropfenwelt_aktualisieren" in s:
        print("scripts.yaml: schon eingetragen"); return
    sichern(SCRI, "tropfenwelt")
    s = SKRIPT.lstrip("\n") if s.strip() in ("", "{}", "[]") else s.rstrip("\n") + "\n" + SKRIPT
    open(SCRI, "w").write(s)
    print("scripts.yaml: Skript eingetragen")

if __name__ == "__main__":
    conf(); automation_weg(); skript()
    print("Fertig. Nach einem Neustart laesst sich der Abgleich mit dem Skript 'Tropfenwelt aktualisieren' ausloesen.")
