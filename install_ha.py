#!/usr/bin/env python3
"""Richtet am Home Assistant den stuendlichen Abgleich ein:
  - shell_command.tropfenwelt_update in configuration.yaml
  - Automation 'Tropfenwelt aktualisieren' in automations.yaml
Legt vorher Sicherungskopien an und aendert nichts, was schon da ist."""
import os, re, shutil, sys

CONF = "/config/configuration.yaml"
AUTO = "/config/automations.yaml"
CMD = '  tropfenwelt_update: "python3 /config/www/tropfenwelt/update.py"'
AUTOMATION = """
- id: tropfenwelt_update
  alias: Tropfenwelt aktualisieren
  description: Holt stuendlich die neueste Fassung des Spiels aus dem GitHub-Repository
  triggers:
    - trigger: time_pattern
      hours: "/1"
  actions:
    - action: shell_command.tropfenwelt_update
  mode: single
"""

def sichern(p):
    if os.path.exists(p) and not os.path.exists(p + ".bak-tropfenwelt"):
        shutil.copy2(p, p + ".bak-tropfenwelt")

def conf():
    s = open(CONF).read() if os.path.exists(CONF) else ""
    if "tropfenwelt_update" in s:
        print("configuration.yaml: schon eingetragen"); return
    sichern(CONF)
    m = re.search(r"^shell_command:[ \t]*$", s, re.M)
    if m:                                   # vorhandenen Block ergaenzen
        s = s[:m.end()] + "\n" + CMD + s[m.end():]
    else:
        s = s.rstrip("\n") + "\n\nshell_command:\n" + CMD + "\n"
    open(CONF, "w").write(s)
    print("configuration.yaml: shell_command eingetragen")

def auto():
    s = open(AUTO).read() if os.path.exists(AUTO) else ""
    if "tropfenwelt_update" in s:
        print("automations.yaml: schon eingetragen"); return
    sichern(AUTO)
    if s.strip() in ("", "[]"):
        s = AUTOMATION.lstrip("\n")
    else:
        s = s.rstrip("\n") + "\n" + AUTOMATION
    open(AUTO, "w").write(s)
    print("automations.yaml: Automation eingetragen")

def pruefen():
    try:
        import yaml
    except ImportError:
        print("Hinweis: yaml-Modul fehlt, Pruefung uebersprungen"); return
    for p in (CONF, AUTO):
        try:
            yaml.safe_load(open(p).read())
            print("YAML in Ordnung:", p)
        except Exception as e:
            print("FEHLER in", p, e); sys.exit(1)

if __name__ == "__main__":
    conf(); auto(); pruefen()
    print("Fertig. Home Assistant einmal neu starten, danach laeuft der Abgleich stuendlich.")
