import base64
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# ============================================
# TEST MODUS - Geen API kosten
# ============================================

def generate_mock_receipt() -> dict:
    """Genereer fake bonnetje data voor testen."""
    stores = [
        ("Albert Heijn", "supermarkt"),
        ("Jumbo", "supermarkt"),
        ("Shell", "tankstation"),
        ("McDonald's", "restaurant"),
        ("HEMA", "overig"),
        ("Kruidvat", "overig"),
        ("Action", "overig"),
    ]

    store_name, category = random.choice(stores)

    # Random datum in de afgelopen 30 dagen
    days_ago = random.randint(0, 30)
    date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # Random items genereren
    possible_items = {
        "supermarkt": [
            ("Melk", 1.89), ("Brood", 2.49), ("Kaas", 4.99),
            ("Appels", 2.29), ("Koffie", 5.99), ("Pasta", 1.29),
        ],
        "tankstation": [
            ("Benzine 40L", 72.50), ("Ruitenwisservloeistof", 4.99),
        ],
        "restaurant": [
            ("Big Mac Menu", 9.95), ("McFlurry", 3.50), ("Koffie", 2.50),
        ],
        "overig": [
            ("Batterijen", 5.99), ("Schrift", 2.49), ("Pen", 1.99),
        ],
    }

    items_pool = possible_items.get(category, possible_items["overig"])
    num_items = random.randint(1, min(4, len(items_pool)))
    selected_items = random.sample(items_pool, num_items)

    items = []
    for desc, price in selected_items:
        qty = random.randint(1, 3) if price < 10 else 1
        items.append({
            "description": desc,
            "quantity": qty,
            "unit_price": price,
            "total_price": round(price * qty, 2),
            "btw_percentage": 9 if category in ["supermarkt", "restaurant"] else 21
        })

    total = sum(item["total_price"] for item in items)
    btw = round(total * 0.09 if category in ["supermarkt", "restaurant"] else total * 0.21 / 1.21, 2)

    payment_method = random.choice(["pin", "pin", "pin", "cash"])  # PIN is meer common

    return {
        "store_name": store_name,
        "date": date,
        "total_amount": round(total, 2),
        "btw_amount": btw,
        "payment_method": payment_method,
        "category": category,
        "items": items,
        "raw_text": f"[TEST MODUS] {store_name} - Fake bonnetje",
        "test_mode": True
    }


async def analyze_receipt_mock(image_path: str) -> dict:
    """Test modus: genereer fake data zonder API calls."""
    return generate_mock_receipt()


# ============================================
# TESSERACT OCR - Gratis lokale OCR
# ============================================

async def analyze_receipt_tesseract(image_path: str) -> dict:
    """
    Analyseer bonnetje met gratis Tesseract OCR.
    Minder nauwkeurig dan OpenAI maar volledig gratis.
    """
    try:
        import pytesseract
        from PIL import Image, ImageEnhance, ImageFilter
    except ImportError:
        return {
            "error": "Tesseract niet geinstalleerd. Run: pip install pytesseract",
            "store_name": None,
            "date": None,
            "total_amount": None,
            "btw_amount": None,
            "payment_method": "onbekend",
            "category": "overig",
            "items": [],
            "raw_text": ""
        }

    # Laad en verbeter de afbeelding voor betere OCR
    img = Image.open(image_path)

    # Converteer naar grayscale
    img = img.convert('L')

    # Verhoog contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    # OCR uitvoeren
    raw_text = pytesseract.image_to_string(img, lang='nld+eng')

    # Probeer data te extraheren uit de tekst
    result = parse_receipt_text(raw_text)
    result["raw_text"] = raw_text

    return result


def parse_receipt_text(text: str) -> dict:
    """Parse OCR tekst en probeer bonnetje data te extraheren."""
    result = {
        "store_name": None,
        "date": None,
        "total_amount": None,
        "btw_amount": None,
        "payment_method": "onbekend",
        "category": "overig",
        "items": []
    }

    lines = text.upper().split('\n')
    text_upper = text.upper()

    # Winkel detectie
    known_stores = {
        "ALBERT HEIJN": ("Albert Heijn", "supermarkt"),
        "JUMBO": ("Jumbo", "supermarkt"),
        "LIDL": ("Lidl", "supermarkt"),
        "ALDI": ("Aldi", "supermarkt"),
        "PLUS": ("Plus", "supermarkt"),
        "SHELL": ("Shell", "tankstation"),
        "BP": ("BP", "tankstation"),
        "ESSO": ("Esso", "tankstation"),
        "TOTAL": ("Total", "tankstation"),
        "MCDONALD": ("McDonald's", "restaurant"),
        "BURGER KING": ("Burger King", "restaurant"),
        "KFC": ("KFC", "restaurant"),
        "HEMA": ("HEMA", "overig"),
        "ACTION": ("Action", "overig"),
        "KRUIDVAT": ("Kruidvat", "overig"),
        "MEDIAMARKT": ("MediaMarkt", "elektronica"),
        "COOLBLUE": ("Coolblue", "elektronica"),
    }

    for store_key, (store_name, category) in known_stores.items():
        if store_key in text_upper:
            result["store_name"] = store_name
            result["category"] = category
            break

    # Datum detectie (verschillende formaten)
    date_patterns = [
        r'(\d{2}[-/]\d{2}[-/]\d{4})',  # DD-MM-YYYY of DD/MM/YYYY
        r'(\d{4}[-/]\d{2}[-/]\d{2})',  # YYYY-MM-DD
        r'(\d{2}[-/]\d{2}[-/]\d{2})',  # DD-MM-YY
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            # Probeer te parsen
            for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%y', '%d/%m/%y']:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    result["date"] = parsed.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
            if result["date"]:
                break

    # Totaal bedrag detectie
    total_patterns = [
        r'TOTAAL[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'TOTAL[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'TE BETALEN[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'BEDRAG[:\s]*[€]?\s*(\d+[.,]\d{2})',
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text_upper)
        if match:
            amount_str = match.group(1).replace(',', '.')
            result["total_amount"] = float(amount_str)
            break

    # BTW detectie
    btw_patterns = [
        r'BTW[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'VAT[:\s]*[€]?\s*(\d+[.,]\d{2})',
    ]

    for pattern in btw_patterns:
        match = re.search(pattern, text_upper)
        if match:
            amount_str = match.group(1).replace(',', '.')
            result["btw_amount"] = float(amount_str)
            break

    # Betaalmethode detectie
    if any(x in text_upper for x in ['PIN', 'MAESTRO', 'VISA', 'MASTERCARD', 'DEBIT', 'CARD']):
        result["payment_method"] = "pin"
    elif any(x in text_upper for x in ['CONTANT', 'CASH', 'CONTACT']):
        result["payment_method"] = "cash"

    return result


# ============================================
# OPENAI VISION - Meest nauwkeurig (betaald)
# ============================================

async def analyze_receipt_openai(image_path: str, api_key: str) -> dict:
    """
    Analyseer een bonnetje foto met OpenAI Vision.
    Extraheert: winkel, datum, totaal, BTW, betaalmethode, items.
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)

    # Lees en encode de afbeelding
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Bepaal het image type
    suffix = Path(image_path).suffix.lower()
    media_type = "image/jpeg"
    if suffix == ".png":
        media_type = "image/png"
    elif suffix == ".webp":
        media_type = "image/webp"

    prompt = """Analyseer dit bonnetje/kassabon en extraheer de volgende informatie in JSON formaat:

{
    "store_name": "naam van de winkel/bedrijf",
    "date": "datum in YYYY-MM-DD formaat",
    "total_amount": getal (totaalbedrag inclusief BTW),
    "btw_amount": getal (BTW bedrag, null als niet zichtbaar),
    "payment_method": "pin" of "cash" of "onbekend",
    "category": "supermarkt" of "restaurant" of "tankstation" of "kleding" of "elektronica" of "overig",
    "items": [
        {
            "description": "omschrijving product",
            "quantity": aantal,
            "unit_price": prijs per stuk,
            "total_price": totaalprijs voor dit item,
            "btw_percentage": BTW percentage (9 of 21, null als onbekend)
        }
    ],
    "raw_text": "alle leesbare tekst van het bonnetje"
}

Let op:
- Bedragen zijn in euro's
- Als iets niet leesbaar is, gebruik null
- Kijk naar aanwijzingen voor betaalmethode: "PIN", "MAESTRO", "VISA", "CONTANT", "CASH", etc.
- Nederlandse bonnetjes hebben vaak 9% BTW (voedsel) of 21% BTW (overig)

Geef ALLEEN de JSON terug, geen andere tekst."""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=2000
    )

    # Parse de JSON response
    content = response.choices[0].message.content.strip()

    # Verwijder eventuele markdown code blocks
    if content.startswith("```"):
        content = re.sub(r"^```json?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {
            "store_name": None,
            "date": None,
            "total_amount": None,
            "btw_amount": None,
            "payment_method": "onbekend",
            "category": "overig",
            "items": [],
            "raw_text": content,
            "error": "Kon bonnetje niet volledig verwerken"
        }

    return result


# ============================================
# HOOFDFUNCTIE - Kiest juiste methode
# ============================================

async def analyze_receipt(image_path: str, api_key: str = None, mode: str = "auto") -> dict:
    """
    Analyseer een bonnetje met de gekozen methode.

    Modes:
    - "test": Fake data, geen API calls (voor ontwikkeling)
    - "tesseract": Gratis lokale OCR (minder nauwkeurig)
    - "openai": OpenAI Vision API (beste kwaliteit, kost geld)
    - "auto": Gebruikt OpenAI als key beschikbaar, anders tesseract
    """
    if mode == "test":
        return await analyze_receipt_mock(image_path)

    elif mode == "tesseract":
        return await analyze_receipt_tesseract(image_path)

    elif mode == "openai":
        if not api_key:
            return {"error": "OpenAI API key vereist voor deze modus"}
        return await analyze_receipt_openai(image_path, api_key)

    else:  # auto
        if api_key:
            return await analyze_receipt_openai(image_path, api_key)
        else:
            return await analyze_receipt_tesseract(image_path)


def format_receipt_summary(data: dict) -> str:
    """Formatteer de bonnetje data als leesbare tekst voor Telegram."""
    lines = []

    # Indicator voor test modus
    if data.get("test_mode"):
        lines.append("🧪 *TEST MODUS - Fake Data*\n")
    else:
        lines.append("📋 *Bonnetje Verwerkt*\n")

    if data.get("store_name"):
        lines.append(f"🏪 *Winkel:* {data['store_name']}")

    if data.get("date"):
        lines.append(f"📅 *Datum:* {data['date']}")

    if data.get("total_amount") is not None:
        lines.append(f"💰 *Totaal:* €{data['total_amount']:.2f}")

    if data.get("btw_amount") is not None:
        lines.append(f"📊 *BTW:* €{data['btw_amount']:.2f}")

    if data.get("payment_method"):
        method_emoji = {
            "pin": "💳",
            "cash": "💵",
            "onbekend": "❓"
        }
        emoji = method_emoji.get(data["payment_method"], "❓")
        lines.append(f"{emoji} *Betaalmethode:* {data['payment_method'].upper()}")

    if data.get("category"):
        lines.append(f"🏷️ *Categorie:* {data['category'].capitalize()}")

    # Items toevoegen als ze er zijn
    items = data.get("items", [])
    if items:
        lines.append("\n📝 *Producten:*")
        for item in items[:10]:
            desc = item.get("description", "Onbekend")
            price = item.get("total_price")
            if price is not None:
                lines.append(f"  • {desc}: €{price:.2f}")
            else:
                lines.append(f"  • {desc}")

        if len(items) > 10:
            lines.append(f"  _...en {len(items) - 10} meer items_")

    if data.get("error"):
        lines.append(f"\n⚠️ _{data['error']}_")

    return "\n".join(lines)
