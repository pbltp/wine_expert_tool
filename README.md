# Wine Expert Tool 🍷

Ein einfaches Bewertungs-Tool für Wein-Visualisierungen.

## Was macht dieses Tool?

1. **Weinbeschreibung eingeben** - Kopiere eine Textbeschreibung eines Weins
2. **Visualisierung generieren** - Das Tool analysiert den Text und generiert eine abstrakte Visualisierung
3. **Bewerten** - Gib 1-5 Sterne und optional einen Kommentar
4. **Statistiken** - Sieh dir die durchschnittliche Qualität und alle bisherigen Bewertungen an

## Installation

```bash
# Python Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

## Starten

```bash
source venv/bin/activate
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## Dateien

- `app.py` - Streamlit Web-App
- `imagegen.py` - Bildgenerierung (Visualisierungs-Engine)
- `text_analyzer.py` - Textanalyse (extrahiert Wein-Parameter aus Beschreibungen)
- `expert_db.py` - SQLite-Datenbank für Bewertungen
- `evaluations.db` - Die Datenbank-Datei (wird automatisch erstellt)

## Bewertungskriterien

Beim Bewerten solltest du beachten:

- **Passt die Farbe?** (Rotwein dunkel, Weißwein hell, etc.)
- **Stimmen die Texturen?** (Mineralisch, fruchtig, etc.)
- **Passt der Restzucker-Balken?** (Trocken vs. Süß)
- **Gesamteindruck?** Spiegelt die Visualisierung den Charakter des Weins wider?
