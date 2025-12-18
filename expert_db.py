"""
SQLite-Datenbank für Experten-Bewertungen der Wein-Visualisierungen.
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


DB_PATH = Path(__file__).parent / "evaluations.db"


def init_db():
    """Erstellt die Datenbank-Tabellen falls sie nicht existieren."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            wine_description TEXT NOT NULL,
            viz_params TEXT NOT NULL,
            image_blob BLOB NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            evaluated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_visualization(description: str, params: Dict[str, Any], image_bytes: bytes) -> int:
    """
    Speichert eine generierte Visualisierung in der Datenbank.
    
    Args:
        description: Die Weinbeschreibung
        params: Die extrahierten Visualisierungs-Parameter als Dict
        image_bytes: Das Bild als PNG-Bytes
        
    Returns:
        Die ID des neuen Eintrags
    """
    import json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        """INSERT INTO evaluations (created_at, wine_description, viz_params, image_blob)
           VALUES (?, ?, ?, ?)""",
        (datetime.now().isoformat(), description, json.dumps(params, ensure_ascii=False), image_bytes)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def save_rating(evaluation_id: int, rating: int, comment: Optional[str] = None):
    """
    Speichert eine Bewertung für eine bestehende Visualisierung.
    
    Args:
        evaluation_id: Die ID der Visualisierung
        rating: Bewertung 1-5 Sterne
        comment: Optionaler Kommentar
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """UPDATE evaluations 
           SET rating = ?, comment = ?, evaluated_at = ?
           WHERE id = ?""",
        (rating, comment, datetime.now().isoformat(), evaluation_id)
    )
    conn.commit()
    conn.close()


def get_all_evaluations() -> List[Dict[str, Any]]:
    """Gibt alle Bewertungen zurück (ohne Bild-Blobs für Performance)."""
    import json
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT id, created_at, wine_description, viz_params, rating, comment, evaluated_at
           FROM evaluations ORDER BY created_at DESC"""
    ).fetchall()
    conn.close()
    
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "wine_description": row["wine_description"],
            "viz_params": json.loads(row["viz_params"]),
            "rating": row["rating"],
            "comment": row["comment"],
            "evaluated_at": row["evaluated_at"],
        })
    return result


def get_evaluation_with_image(evaluation_id: int) -> Optional[Dict[str, Any]]:
    """Gibt eine einzelne Bewertung inkl. Bild zurück."""
    import json
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """SELECT * FROM evaluations WHERE id = ?""",
        (evaluation_id,)
    ).fetchone()
    conn.close()
    
    if row is None:
        return None
    
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "wine_description": row["wine_description"],
        "viz_params": json.loads(row["viz_params"]),
        "image_blob": row["image_blob"],
        "rating": row["rating"],
        "comment": row["comment"],
        "evaluated_at": row["evaluated_at"],
    }


def get_unevaluated_count() -> int:
    """Gibt die Anzahl der noch nicht bewerteten Visualisierungen zurück."""
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM evaluations WHERE rating IS NULL"
    ).fetchone()[0]
    conn.close()
    return count


def get_statistics() -> Dict[str, Any]:
    """Gibt Statistiken über alle Bewertungen zurück."""
    conn = sqlite3.connect(DB_PATH)
    
    total = conn.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
    evaluated = conn.execute("SELECT COUNT(*) FROM evaluations WHERE rating IS NOT NULL").fetchone()[0]
    avg_rating = conn.execute("SELECT AVG(rating) FROM evaluations WHERE rating IS NOT NULL").fetchone()[0]
    
    rating_dist = {}
    for i in range(1, 6):
        count = conn.execute("SELECT COUNT(*) FROM evaluations WHERE rating = ?", (i,)).fetchone()[0]
        rating_dist[i] = count
    
    conn.close()
    
    return {
        "total": total,
        "evaluated": evaluated,
        "unevaluated": total - evaluated,
        "avg_rating": round(avg_rating, 2) if avg_rating else None,
        "rating_distribution": rating_dist,
    }


def delete_evaluation(evaluation_id: int):
    """Löscht eine Bewertung."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM evaluations WHERE id = ?", (evaluation_id,))
    conn.commit()
    conn.close()


# Initialisiere DB beim Import
init_db()
