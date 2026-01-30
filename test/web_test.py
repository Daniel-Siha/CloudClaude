#!/usr/bin/env python3
"""
Web interface om bonnetjes OCR te testen.

Start met:
    pip install streamlit
    streamlit run test/web_test.py
"""

import sys
import os
import json
import tempfile

# Voeg src toe aan path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import asyncio

from src.ocr import analyze_receipt, format_receipt_summary


st.set_page_config(
    page_title="Bonnetjes Scanner Test",
    page_icon="🧾",
    layout="wide"
)

st.title("🧾 Bonnetjes Scanner Test")
st.markdown("Upload een foto van een bonnetje om te zien hoe de OCR het verwerkt.")

# Sidebar voor instellingen
st.sidebar.header("⚙️ Instellingen")

ocr_mode = st.sidebar.selectbox(
    "OCR Modus",
    options=["test", "tesseract", "openai"],
    format_func=lambda x: {
        "test": "🧪 Test (fake data - gratis)",
        "tesseract": "🔍 Tesseract (echte OCR - gratis)",
        "openai": "🤖 OpenAI Vision (beste - ~€0.02)"
    }[x]
)

# Check OpenAI key
openai_key = os.getenv("OPENAI_API_KEY")
if ocr_mode == "openai":
    if not openai_key or openai_key == "your_openai_api_key_here":
        st.sidebar.error("⚠️ OpenAI API key niet geconfigureerd in .env")
        st.sidebar.code("OPENAI_API_KEY=sk-...")
    else:
        st.sidebar.success("✅ OpenAI API key gevonden")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Modi uitleg:**
- **Test**: Genereert fake data, geen echte OCR
- **Tesseract**: Gratis lokale OCR (matige kwaliteit)
- **OpenAI**: Beste kwaliteit, kost ~€0.01-0.03 per foto
""")

# File upload
uploaded_file = st.file_uploader(
    "Upload een bonnetje foto",
    type=["jpg", "jpeg", "png", "webp"],
    help="Ondersteunde formaten: JPG, PNG, WebP"
)

if uploaded_file is not None:
    # Toon de geüploade foto
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Geüploade foto")
        st.image(uploaded_file, use_container_width=True)

    with col2:
        st.subheader("📋 Extractie resultaat")

        # Verwerk knop
        if st.button("🔍 Analyseer bonnetje", type="primary", use_container_width=True):
            with st.spinner(f"Bezig met {ocr_mode.upper()} analyse..."):
                # Sla tijdelijk op
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                try:
                    # Run OCR
                    api_key = openai_key if ocr_mode in ["openai", "auto"] else None
                    result = asyncio.run(analyze_receipt(tmp_path, api_key, mode=ocr_mode))

                    # Toon test mode warning
                    if result.get("test_mode"):
                        st.warning("🧪 TEST MODUS - Dit is fake data, niet van je foto!")

                    # Toon resultaten in nette boxes
                    if result.get("store_name"):
                        st.metric("🏪 Winkel", result["store_name"])

                    mcol1, mcol2 = st.columns(2)
                    with mcol1:
                        if result.get("date"):
                            st.metric("📅 Datum", result["date"])
                        if result.get("total_amount") is not None:
                            st.metric("💰 Totaal", f"€{result['total_amount']:.2f}")
                    with mcol2:
                        if result.get("btw_amount") is not None:
                            st.metric("📊 BTW", f"€{result['btw_amount']:.2f}")
                        if result.get("payment_method"):
                            emoji = {"pin": "💳", "cash": "💵", "onbekend": "❓"}.get(result["payment_method"], "❓")
                            st.metric(f"{emoji} Betaalmethode", result["payment_method"].upper())

                    if result.get("category"):
                        st.metric("🏷️ Categorie", result["category"].capitalize())

                    # Items
                    items = result.get("items", [])
                    if items:
                        st.markdown("**📝 Producten:**")
                        for item in items:
                            price = item.get("total_price")
                            desc = item.get("description", "Onbekend")
                            qty = item.get("quantity", 1)
                            if price is not None:
                                st.markdown(f"- {desc} (x{qty}): €{price:.2f}")
                            else:
                                st.markdown(f"- {desc} (x{qty})")

                    # Error
                    if result.get("error"):
                        st.error(f"⚠️ {result['error']}")

                finally:
                    # Cleanup
                    os.unlink(tmp_path)

                # Toon ruwe JSON in expander
                with st.expander("🔧 Ruwe JSON data"):
                    # Verwijder raw_text voor leesbaarheid
                    display_result = {k: v for k, v in result.items() if k != "raw_text"}
                    st.json(display_result)

                # Toon raw text als beschikbaar
                if result.get("raw_text") and not result.get("test_mode"):
                    with st.expander("📝 OCR ruwe tekst"):
                        st.text(result["raw_text"])

else:
    # Placeholder
    st.info("👆 Upload een foto van een bonnetje om te beginnen")

    # Voorbeeld
    st.markdown("---")
    st.subheader("📌 Wat wordt er geëxtraheerd?")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Basis info:**
        - Winkelnaam
        - Datum
        - Totaalbedrag
        - BTW bedrag
        """)
    with col2:
        st.markdown("""
        **Betaling:**
        - PIN / Cash / Onbekend
        - Categorie (supermarkt, restaurant, etc.)
        """)
    with col3:
        st.markdown("""
        **Producten:**
        - Omschrijving
        - Aantal
        - Prijs per stuk
        - Totaalprijs
        """)
