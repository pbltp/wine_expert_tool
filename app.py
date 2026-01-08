"""
Wine Expert Tool - Streamlit App
Interaktive Bewertung von Wein-Visualisierungen durch Experten.
"""
import streamlit as st
from io import BytesIO
import expert_db as db
from text_analyzer import analyze_wine_description
from imagegen import generate_wine_png_bytes
from imagefetch import generate_wine_external_api
import base64

cookie = base64.b64encode(b'bWVnc3plbnRzZWd0ZWxlbml0').decode('ascii')

st.set_page_config(
    page_title="🍷 Wine Expert Tool",
    page_icon="🍷",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialisierung
# ─────────────────────────────────────────────────────────────────────────────
if "current_viz" not in st.session_state:
    st.session_state.current_viz = None  # {"id": ..., "image_bytes": ..., "params": ...}
if "show_history" not in st.session_state:
    st.session_state.show_history = False


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar: Statistiken & Navigation
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Statistiken")
    stats = db.get_statistics()
    
    col1, col2 = st.columns(2)
    col1.metric("Gesamt", stats["total"])
    col2.metric("Bewertet", stats["evaluated"])
    
    if stats["avg_rating"]:
        st.metric("⭐ Durchschnitt", f"{stats['avg_rating']:.1f}")
    
    st.divider()
    
    if st.button("📜 Bisherige Bewertungen", width="content"):
        st.session_state.show_history = not st.session_state.show_history
    
    if stats["unevaluated"] > 0:
        st.warning(f"🔔 {stats['unevaluated']} unbewertete Visualisierungen")


# ─────────────────────────────────────────────────────────────────────────────
# History View
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_history:
    st.title("📜 Bisherige Bewertungen")
    
    evaluations = db.get_all_evaluations()
    
    if not evaluations:
        st.info("Noch keine Bewertungen vorhanden.")
    else:
        for ev in evaluations:
            with st.expander(f"ID {ev['id']} - {ev['created_at'][:10]} - {'⭐' * (ev['rating'] or 0) or '❓ Unbewertet'}"):
                st.text(ev["wine_description"][:200] + "..." if len(ev["wine_description"]) > 200 else ev["wine_description"])
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if ev["comment"]:
                        st.caption(f"💬 {ev['comment']}")
                with col2:
                    if st.button("🖼️ Anzeigen", key=f"show_{ev['id']}"):
                        full_ev = db.get_evaluation_with_image(ev["id"])
                        st.session_state.current_viz = {
                            "id": full_ev["id"],
                            "image_bytes": full_ev["image_blob"],
                            "params": full_ev["viz_params"],
                            "description": full_ev["wine_description"],
                            "existing_rating": full_ev["rating"],
                            "existing_comment": full_ev["comment"],
                        }
                        st.session_state.show_history = False
                        st.rerun()
    
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# Main View: Neue Visualisierung erstellen
# ─────────────────────────────────────────────────────────────────────────────
st.title("🍷 Wine Expert Tool")
st.caption("Bewerte die Qualität der automatischen Wein-Visualisierungen")

# ─────────────────────────────────────────────────────────────────────────────
# Eingabe-Bereich
# ─────────────────────────────────────────────────────────────────────────────
wine_description = st.text_area(
    "Weinbeschreibung eingeben:",
    height=150,
    placeholder="Füge hier eine Weinbeschreibung ein...\n\nz.B. 'Ein eleganter Pinot Noir aus dem Burgund mit Aromen von Kirsche und Himbeere, feinen Tanninen und einem langen Abgang...'",
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    generate_btn = st.button("🎨 Visualisierungen generieren", type="primary", width="content")

with col2:
    if st.session_state.current_viz:
        clear_btn = st.button("🗑️ Zurücksetzen", width="content")
        if clear_btn:
            st.session_state.current_viz = None
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Generierung
# ─────────────────────────────────────────────────────────────────────────────
if generate_btn:
    if not wine_description.strip():
        st.error("Bitte gib eine Weinbeschreibung ein.")
    else:
        with st.spinner("Analysiere Beschreibung und generiere Visualisierung..."):
            # Analysiere Text
            params = analyze_wine_description(wine_description)
            
            # Generiere Bild (generate_wine_png_bytes erwartet ein dict)
            image_bytes = generate_wine_png_bytes(params, size=350)
            
            # In DB speichern
            new_id = db.save_visualization(wine_description, params, image_bytes)

            # Generiere Bild (mit anderen API)
            new_id2 = None
            image_bytes2 = None
            try:
                image_bytes2 = generate_wine_external_api(wine_description, cookie)

                new_id2 = db.save_visualization(wine_description, params, image_bytes2)
            except Exception as e:
                print(e)
                pass

            st.session_state.current_viz = {
                "id": new_id,
                "id2": new_id2,
                "image_bytes": image_bytes,
                "image_bytes2": image_bytes2,
                "params": params,
                "description": wine_description,
                "existing_rating": None,
                "existing_comment": None,
                "existing_rating2": None,
                "existing_comment2": None,
            }
            
        st.success(f"✅ Visualisierung generiert! (ID: {new_id})")
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Anzeige & Bewertung
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.current_viz:
    viz = st.session_state.current_viz
    
    st.divider()
    st.subheader("🖼️ Generierte Visualisierungen")
    
    col_img, col_eval = st.columns([2, 1])
    
    with col_img:
        st.divider()
        st.image(viz["image_bytes"], width="content")
        
        # Parameter anzeigen
        with st.expander("📐 Extrahierte Parameter"):
            params = viz["params"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Basisfarbe:** {params['base_color_hex']}")
                st.write(f"**Säure:** {params['acidity']:.1%}")
                st.write(f"**Körper:** {params['body']:.1%}")
                st.write(f"**Tannin:** {params['tannin']:.1%}")
            with col2:
                st.write(f"**Tiefe:** {params['depth']:.1%}")
                st.write(f"**Süße:** {params['sweetness']:.1%}")
                st.write(f"**Holz:** {params['oak_intensity']:.1%}")
                st.write(f"**Perlage:** {params['effervescence']:.1%}")
            with col3:
                st.write(f"**Mineralik:** {params['mineral_intensity']:.1%}")
                st.write(f"**Restzucker:** {params['residual_sugar']:.0f} g/L")
                st.write(f"**Weintyp:** {params['wine_type']}")
    
    with col_eval:
        st.subheader("⭐ Bewertung")
        
        # Star Rating
        rating = st.radio(
            "Wie gut passt die Visualisierung zur Beschreibung?",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            horizontal=True,
            index=(viz["existing_rating"] - 1) if viz["existing_rating"] else 2,
        )
        
        # Kommentar
        comment = st.text_area(
            "Kommentar (optional):",
            value=viz["existing_comment"] or "",
            height=100,
            placeholder="Was passt gut? Was könnte besser sein?",
        )
        
        # Bewertung speichern
        if st.button("💾 Bewertung speichern", type="primary", width="content"):
            db.save_rating(viz["id"], rating, comment if comment.strip() else None)
            st.success("✅ Bewertung gespeichert!")
            st.session_state.current_viz["existing_rating"] = rating
            st.session_state.current_viz["existing_comment"] = comment
            st.rerun()

    if "id2" in viz and viz["id2"] != None:
        st.divider()
        col_img2, col_eval2 = st.columns([2, 1])

        with col_img2:
            st.image(viz["image_bytes2"], width="content")

        with col_eval2:
            # Star Rating
            rating2 = st.radio(
                "Wie gut passt die Visualisierung zur Beschreibung?",
                key="radio2",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "⭐" * x,
                horizontal=True,
                index=(viz["existing_rating2"] - 1) if viz["existing_rating2"] else 2,
            )

            # Kommentar
            comment2 = st.text_area(
                "Kommentar (optional):",
                key="comment2",
                value=viz["existing_comment"] or "",
                height=100,
                placeholder="Was passt gut? Was könnte besser sein?",
            )

            # Bewertung speichern
            if st.button("💾 Bewertung speichern", type="primary", width="content", key="button2"):
                db.save_rating(viz["id2"], rating2, comment2 if comment2.strip() else None)
                st.success("✅ Bewertung gespeichert!")
                st.session_state.current_viz["existing_rating2"] = rating2
                st.session_state.current_viz["existing_comment2"] = comment2
                st.rerun()

    # Löschen
    st.divider()
    if st.button("🗑️ Eintrag löschen", width="content"):
        db.delete_evaluation(viz["id"])
        if "id2" in viz:
            db.delete_evaluation(viz["id2"])
        st.session_state.current_viz = None
        st.warning("Eintrag gelöscht.")
        st.rerun()
