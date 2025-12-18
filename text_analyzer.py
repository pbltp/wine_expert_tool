"""
Text-Analyse: Extrahiert Visualisierungs-Parameter aus Weinbeschreibungen.
Basiert auf der Heuristik aus bsp_runner.py
"""
from typing import Dict


def _score(text: str, words: list[str]) -> float:
    """Zählt wie viele Wörter aus der Liste im Text vorkommen."""
    t = text.lower()
    hits = sum(1 for w in words if w in t)
    return min(1.0, hits / max(1, len(words)))


def analyze_wine_description(txt: str) -> Dict:
    """
    Analysiert eine Weinbeschreibung und extrahiert Visualisierungs-Parameter.
    
    Args:
        txt: Freitext-Beschreibung eines Weins
        
    Returns:
        Dict mit allen viz-Parametern für imagegen
    """
    t = txt.lower()

    # === Basisfarbe: Zuerst Weintyp bestimmen ===
    
    # Rosé erkennen
    is_rose = any(k in t for k in ["rosé", "rose ", "lachsrosa", "rosa"])
    
    # Rotwein erkennen (Rebsorten und Beschreibungen)
    red_grapes = ["pinot noir", "merlot", "cabernet", "blaufränkisch", "zweigelt", 
                  "sangiovese", "nebbiolo", "tempranillo", "syrah", "shiraz",
                  "grenache", "mourvèdre", "tignanello", "st. laurent"]
    red_descriptors = ["rubinrot", "purpur", "violett", "dunkelrot", "schwarz-violett",
                       "rubin", "granat", "tiefdunkel", "kirschrot"]
    is_red = any(k in t for k in red_grapes) or any(k in t for k in red_descriptors)
    
    # Weißwein erkennen (Rebsorten)
    white_grapes = ["chardonnay", "riesling", "sauvignon blanc", "grüner veltliner",
                    "weißburgunder", "pinot grigio", "pinot gris", "welschriesling",
                    "gewürztraminer", "muskateller", "grauburgunder", "albariño"]
    white_descriptors = ["zitronengelb", "grüngelb", "strohgelb", "goldgelb", 
                         "blassgelb", "hellgelb", "grünliche reflexe"]
    is_white = any(k in t for k in white_grapes) or any(k in t for k in white_descriptors)
    
    # Süßwein/Amber erkennen
    is_sweet_amber = any(k in t for k in ["trockenbeerenauslese", "beerenauslese", 
                                           "eiswein", "auslese", "bernstein", 
                                           "amber", "goldgelb mit bernstein"])

    # Basisfarbe zuweisen
    wine_type = "auto"
    if is_rose:
        base_color = "#C8857F"
        wine_type = "rose"
    elif is_red:
        if "pinot noir" in t:
            base_color = "#8A3050"
        elif "zweigelt" in t:
            base_color = "#8A2540"
        elif any(k in t for k in ["tignanello", "sangiovese"]):
            base_color = "#6B1528"
        elif any(k in t for k in ["tiefdunkel", "schwarz", "dicht", "ducru", "château"]):
            base_color = "#4A0D1C"
        else:
            base_color = "#7A1024"
        wine_type = "red"
    elif is_sweet_amber:
        base_color = "#E8C070"
        wine_type = "white"
    elif is_white:
        if any(k in t for k in ["grüngelb", "grünliche reflexe", "sauvignon"]):
            base_color = "#E8EDB3"
        elif any(k in t for k in ["strohgelb", "weißburgunder", "pinot grigio"]):
            base_color = "#F0E6B8"
        else:
            base_color = "#F6F2AF"
        wine_type = "white"
    else:
        base_color = "#F6F2AF"
        wine_type = "white"

    # Scores für Dimensionen
    acidity = _score(t, ["frisch", "säure", "frische", "zitrus", "lime", "limette", "knackig", "rassig"])
    body = _score(t, ["voll", "kräftig", "opulent", "cremig", "dicht", "schmelz", "struktur"])
    tannin = _score(t, ["tannin", "gerbstoff", "griffig", "feinkörnig", "adstringierend", "gerbstoffe"])
    depth = _score(t, ["komplex", "tiefe", "vielschichtig", "lang", "nachhall", "intensiv"])
    sweetness = _score(t, ["lieblich", "süß", "süss", "edelsüß", "spätlese", "beerenauslese", "eiswein", "honig"])
    
    # Restzucker in g/L schätzen
    residual_sugar = 0.0
    if any(k in t for k in ["trockenbeerenauslese", "tba"]):
        residual_sugar = 300.0
    elif any(k in t for k in ["beerenauslese", "eiswein"]):
        residual_sugar = 180.0
    elif any(k in t for k in ["auslese"]):
        residual_sugar = 80.0
    elif any(k in t for k in ["spätlese"]):
        residual_sugar = 40.0
    elif any(k in t for k in ["lieblich", "feinherb", "restsüß", "restzucker"]):
        residual_sugar = 25.0
    elif any(k in t for k in ["halbtrocken", "off-dry"]):
        residual_sugar = 12.0
    elif any(k in t for k in ["trocken", "dry", "brut"]):
        residual_sugar = 4.0
    else:
        residual_sugar = 6.0

    # Holz / Ausbau
    oak_intensity = 0.0
    if any(k in t for k in ["barrique", "holzfass", "eichenfass", "fassausbau", "oak"]):
        oak_intensity = 0.7
    if any(k in t for k in ["stahltank", "edelstahl", "stainless steel"]):
        oak_intensity = max(oak_intensity, 0.2)

    # Perlage / Spritzigkeit
    effervescence = 0.0
    if any(k in t for k in ["champagner", "champagne"]):
        effervescence = 1.0
    elif any(k in t for k in ["schaumwein", "sekt", "crémant", "cava", "sparkling", "perlage"]):
        effervescence = 0.8
    elif any(k in t for k in ["perlwein", "frizzante", "prosecco", "petillant"]):
        effervescence = 0.5
    elif any(k in t for k in ["leicht perlend", "spritzig", "prickelnd"]):
        effervescence = 0.3

    # Mineralik
    mineral_intensity = _score(t, ["mineral", "mineralisch", "schiefer", "kreide", "steinig", "salzig"])

    # Frucht-Cluster
    fruit_citrus = _score(t, ["zitrus", "zitrone", "limette", "grapefruit", "lime"])
    fruit_stone = _score(t, ["pfirsich", "aprikose", "nektarine", "marille"])
    fruit_tropical = _score(t, ["ananas", "mango", "maracuja", "passionsfrucht", "lychee", "litschi"])
    fruit_red = _score(t, ["erdbeere", "himbeere", "kirsche", "rote beeren", "strawberry", "raspberry", "cherry"])
    fruit_dark = _score(t, ["blaubeere", "heidelbeere", "brombeere", "schwarze johannisbeere", "pflaume", "plum", "blackberry"])

    # Kräuter & Würze
    herbal_intensity = _score(t, ["gras", "kräuter", "heu", "heublume", "minze", "krautig", "floral", "blume"])
    spice_intensity = _score(t, ["gewürz", "pfeffer", "zimt", "nelke", "muskat", "würzig"])

    return {
        "base_color_hex": base_color,
        "wine_type": wine_type,
        "acidity": max(0.2, min(1.0, acidity + 0.1)),
        "body": max(0.2, min(1.0, body + 0.1)),
        "tannin": tannin,
        "depth": max(0.2, depth),
        "sweetness": sweetness,
        "oak_intensity": oak_intensity,
        "effervescence": effervescence,
        "mineral_intensity": mineral_intensity,
        "herbal_intensity": herbal_intensity,
        "spice_intensity": spice_intensity,
        "fruit_citrus": fruit_citrus,
        "fruit_stone": fruit_stone,
        "fruit_tropical": fruit_tropical,
        "fruit_red": fruit_red,
        "fruit_dark": fruit_dark,
        "residual_sugar": residual_sugar,
    }
