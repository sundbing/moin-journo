# moin-journo

Eine kleine Sammlung von „Moin“-Wörtern und -Redewendungen mit kurzen Erklärungen (Deutsch).

## Dateien
- `moin.md`: Hauptinhalt mit Wörtern/Redewendungen und Notizen.

## Änderungen committen (GitHub)

Nachfolgend findest du einen üblichen Workflow mit Git und GitHub. Wenn du neu bei Git bist, führe die Schritte unter „Ersteinrichtung“ einmalig aus.

### Ersteinrichtung
1. Git installieren: https://git-scm.com/downloads
2. Identität konfigurieren (einmal pro Rechner):
```bash
git config --global user.name "Dein Name"
git config --global user.email "du@example.com"
```
3. (Optional) Nützliche Defaults setzen:
```bash
git config --global pull.rebase false
git config --global init.defaultBranch main
```

### Code holen
- Wenn du noch nicht geklont hast:
```bash
git clone https://github.com/sundbing/moin-journo.git
cd moin-journo
```
- Wenn du schon geklont hast, lokale Kopie aktualisieren:
```bash
git pull
```

### Branch erstellen (empfohlen)
Ein Feature-Branch hält `main` sauber.
```bash
git checkout -b feat/update-moin-list
```

### Änderungen machen
Dateien bearbeiten (z. B. `moin.md` oder `README.md` aktualisieren).

### Änderungen ansehen
```bash
git status
git diff   # optional
```

### Stagen und committen
- Bestimmte Dateien stagen:
```bash
git add moin.md   # oder alle geänderten Dateien
```
- Mit klarer Nachricht committen:
```bash
git commit -m "Add new Moin expressions and explanations"
```

Tipps für gute Commit-Messages:
- Imperativ verwenden ("Add", "Fix", "Update").
- Betreffzeile ~72 Zeichen; Details ggf. in den Body.

### Branch pushen
```bash
git push -u origin feat/update-moin-list
```

### Pull Request (PR) eröffnen
1. Repository auf GitHub öffnen.
2. Hinweis zum neuen Branch nutzen: „Compare & pull request“.
3. Titel und Beschreibung ausfüllen, ggf. Issues verlinken.
4. PR zur Review einreichen.

### PR mergen
- Nach Freigabe und ggf. erfolgreichen Checks auf „Merge“ klicken.
- Branch auf GitHub löschen (optional).
- Lokales `main` aktualisieren:
```bash
git checkout main
git pull
```

### Kleine Änderungen per Web-UI (Alternative)
- Auf GitHub zur Datei navigieren (z. B. `moin.md`).
- Stiftsymbol klicken und bearbeiten.
- GitHub erstellt beim Speichern automatisch einen Branch und PR.

## Hinweise
- Dieses Repository nutzt GitHub; überprüfe, dass `origin` korrekt gesetzt ist:
```bash
git remote -v
```
- Wenn du über einen Fork beiträgst, `origin` auf deinen Fork setzen und das Upstream-Repo hinzufügen:
```bash
git remote add upstream https://github.com/sundbing/moin-journo.git
# In Sync bleiben:
git fetch upstream
git checkout main
git merge upstream/main
```