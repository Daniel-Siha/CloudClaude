#!/usr/bin/env python3
"""
Test script voor OCR bonnetjes extractie.

Gebruik:
    python test/test_ocr.py                     # Test modus (fake data)
    python test/test_ocr.py foto.jpg            # Test met een echte foto
    python test/test_ocr.py foto.jpg tesseract  # Test met Tesseract OCR
    python test/test_ocr.py foto.jpg openai     # Test met OpenAI (kost geld!)
"""

import asyncio
import json
import sys
import os

# Voeg src toe aan path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from src.ocr import analyze_receipt, format_receipt_summary


async def test_ocr(image_path: str = None, mode: str = "test"):
    """Test de OCR functie."""

    print("=" * 50)
    print(f"🧪 OCR Test - Modus: {mode.upper()}")
    print("=" * 50)

    if image_path:
        print(f"📷 Foto: {image_path}")
        if not os.path.exists(image_path):
            print(f"❌ Bestand niet gevonden: {image_path}")
            return
    else:
        print("📷 Geen foto opgegeven, gebruik test modus met fake data")
        mode = "test"

    print("\n⏳ Bezig met verwerken...\n")

    # Haal API key op indien nodig
    api_key = os.getenv("OPENAI_API_KEY") if mode in ["openai", "auto"] else None

    if mode == "openai" and not api_key:
        print("❌ OpenAI API key niet gevonden in .env bestand!")
        print("   Gebruik 'test' of 'tesseract' modus, of voeg OPENAI_API_KEY toe.")
        return

    # Voer OCR uit
    result = await analyze_receipt(image_path or "dummy.jpg", api_key, mode=mode)

    # Toon geformatteerde output (zoals in Telegram)
    print("📋 TELEGRAM OUTPUT:")
    print("-" * 50)
    print(format_receipt_summary(result))
    print("-" * 50)

    # Toon ruwe JSON data
    print("\n📊 RUWE DATA (JSON):")
    print("-" * 50)
    # Verwijder raw_text voor leesbaarheid (kan heel lang zijn)
    display_result = {k: v for k, v in result.items() if k != "raw_text"}
    print(json.dumps(display_result, indent=2, ensure_ascii=False))

    # Toon raw_text apart als die er is
    if result.get("raw_text") and mode != "test":
        print("\n📝 RUWE TEKST (OCR output):")
        print("-" * 50)
        print(result["raw_text"][:500])
        if len(result.get("raw_text", "")) > 500:
            print(f"... ({len(result['raw_text'])} karakters totaal)")

    print("\n✅ Test voltooid!")


def main():
    # Parse argumenten
    image_path = None
    mode = "test"

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        # Als het een mode is ipv een bestand
        if image_path in ["test", "tesseract", "openai", "auto"]:
            mode = image_path
            image_path = None

    if len(sys.argv) > 2:
        mode = sys.argv[2]

    # Run async functie
    asyncio.run(test_ocr(image_path, mode))


if __name__ == "__main__":
    main()
