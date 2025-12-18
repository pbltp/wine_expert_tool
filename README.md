# Wine Expert Tool 🍷

Ein interaktives Bewertungs-Tool für Wein-Visualisierungen. Entwickelt für Wein-Experten, um die Qualität automatisch generierter Wein-Visualisierungen zu evaluieren.

## 🎯 Was macht dieses Tool?

Das Tool generiert abstrakte visuelle Darstellungen von Weinen basierend auf Textbeschreibungen. Experten können diese Visualisierungen bewerten, um die Qualität des Algorithmus zu verbessern.

**Workflow:**
1. **Weinbeschreibung eingeben** → Kopiere eine Textbeschreibung eines Weins
2. **Visualisierung generieren** → Das Tool analysiert den Text und erstellt ein Bild
3. **Bewerten** → Vergib 1-5 Sterne und optional einen Kommentar
4. **Statistiken ansehen** → Sieh dir alle bisherigen Bewertungen an

---

## 🚀 Installation

### Voraussetzungen
- Python 3.10 oder neuer
- macOS, Linux oder Windows

### Schritt 1: Repository klonen
```bash
git clone https://github.com/ghmbacher/wine_expert_tool.git
cd wine_expert_tool
```

### Schritt 2: Virtual Environment erstellen
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat
```

### Schritt 3: Dependencies installieren
```bash
pip install -r requirements.txt
```

---

## ▶️ Starten

```bash
# Virtual Environment aktivieren (falls noch nicht aktiv)
source venv/bin/activate  # macOS/Linux
# oder: .\venv\Scripts\Activate.ps1  # Windows

# App starten
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter: **http://localhost:8501**

Falls der Port belegt ist:
```bash
streamlit run app.py --server.port 8502
```

---

## 📖 Bedienung

### Neue Visualisierung erstellen
1. Füge eine Weinbeschreibung in das Textfeld ein
2. Klicke auf **"🎨 Visualisierung generieren"**
3. Das Bild wird generiert und angezeigt

### Bewertung abgeben
1. Wähle 1-5 Sterne (⭐ bis ⭐⭐⭐⭐⭐)
2. Schreibe optional einen Kommentar
3. Klicke auf **"💾 Bewertung speichern"**

### Statistiken & Historie
- Die **Sidebar links** zeigt Statistiken (Anzahl, Durchschnitt)
- Klicke auf **"📜 Bisherige Bewertungen"** um alle Einträge zu sehen
- Klicke auf **"🖼️ Anzeigen"** um eine alte Visualisierung erneut anzuzeigen

---

## 🎨 Bewertungskriterien

Beim Bewerten solltest du folgende Aspekte berücksichtigen:

| Kriterium | Beschreibung |
|-----------|--------------|
| **Farbe** | Passt die Grundfarbe zum Weintyp? (Rot dunkel, Weiß hell, Rosé rosa) |
| **Texturen** | Spiegeln die Texturen die Eigenschaften wider? (Mineralik, Frucht, Tannine) |
| **Restzucker-Balken** | Zeigt der rechte Balken den korrekten Süßegrad? |
| **Gesamteindruck** | Vermittelt das Bild den Charakter des Weins? |

**Bewertungsskala:**
- ⭐ = Komplett falsch
- ⭐⭐ = Wenig passend
- ⭐⭐⭐ = Teilweise passend
- ⭐⭐⭐⭐ = Gut passend
- ⭐⭐⭐⭐⭐ = Perfekt

---

## 📁 Projektstruktur

```
wine_expert_tool/
├── app.py              # Streamlit Web-App (Hauptanwendung)
├── imagegen.py         # Bildgenerierungs-Engine
├── text_analyzer.py    # Textanalyse (extrahiert Wein-Parameter)
├── expert_db.py        # SQLite-Datenbank für Bewertungen
├── requirements.txt    # Python Dependencies
├── evaluations.db      # Datenbank (wird automatisch erstellt)
└── README.md           # Diese Datei
```

---

## 🔧 Technische Details

### Extrahierte Parameter

Die Textanalyse extrahiert folgende Parameter aus Weinbeschreibungen:

| Parameter | Beschreibung | Wertebereich |
|-----------|--------------|--------------|
| `base_color_hex` | Basisfarbe des Weins | Hex-Farbe |
| `acidity` | Säure | 0.0 - 1.0 |
| `body` | Körper/Fülle | 0.0 - 1.0 |
| `tannin` | Tannine (Gerbstoffe) | 0.0 - 1.0 |
| `residual_sugar` | Restzucker | 0 - 500 g/L |
| `oak_intensity` | Holzausbau | 0.0 - 1.0 |
| `effervescence` | Perlage/Kohlensäure | 0.0 - 1.0 |
| `mineral_intensity` | Mineralik | 0.0 - 1.0 |
| `fruit_citrus` | Zitrusfrüchte | 0.0 - 1.0 |
| `fruit_stone` | Steinobst | 0.0 - 1.0 |
| `fruit_tropical` | Tropische Früchte | 0.0 - 1.0 |
| `fruit_red` | Rote Beeren | 0.0 - 1.0 |
| `fruit_dark` | Dunkle Beeren | 0.0 - 1.0 |

### Datenbank

Die Bewertungen werden in einer SQLite-Datenbank (`evaluations.db`) gespeichert:

```sql
evaluations (
    id              INTEGER PRIMARY KEY,
    created_at      TEXT,           -- Erstellungszeitpunkt
    wine_description TEXT,          -- Originale Beschreibung
    viz_params      TEXT,           -- Extrahierte Parameter (JSON)
    image_blob      BLOB,           -- Generiertes Bild (PNG)
    rating          INTEGER,        -- 1-5 Sterne
    comment         TEXT,           -- Kommentar
    evaluated_at    TEXT            -- Bewertungszeitpunkt
)
```

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
→ Virtual Environment aktivieren: `source venv/bin/activate`

### Port 8501 ist belegt
→ Anderen Port verwenden: `streamlit run app.py --server.port 8502`

### Bild wird nicht generiert
→ Prüfe ob alle Dependencies installiert sind: `pip install -r requirements.txt`

### Datenbank zurücksetzen
→ Lösche die Datei `evaluations.db` - sie wird beim nächsten Start neu erstellt

---

## 📝 Beispiel-Beschreibungen zum Testen

**Rotwein (trocken):**
```
Ein eleganter Pinot Noir aus dem Burgund mit Aromen von Kirsche und Himbeere, 
feinen Tanninen und einem langen Abgang. Leichte Noten von Unterholz und Gewürzen.
```

**Weißwein (trocken):**
```
Frischer Grüner Veltliner mit pfeffrigen Noten und Zitrusaromen. 
Knackige Säure, mineralischer Abgang. Perfekt zu Spargel.
```

**Süßwein:**
```
Trockenbeerenauslese aus dem Burgenland, goldgelb mit Bernsteintönen.
Intensive Aromen von Honig, getrockneten Aprikosen und Orangenzesten.
Opulente Süße mit balancierender Säure.
```

---

## 👥 Kontakt

Bei Fragen oder Problemen wende dich an das Entwicklerteam.

---

*Entwickelt für das Colours of Wine Projekt*
