import base64
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# ============================================
# HORECA LEVERANCIERS & CATEGORIEËN
# ============================================

HORECA_SUPPLIERS = {
    "SLIGRO": "groothandel",
    "MAKRO": "groothandel",
    "HANOS": "groothandel",
    "BIDFOOD": "groothandel",
    "DELI XL": "groothandel",
    "ALBERT HEIJN": "supermarkt",
    "JUMBO": "supermarkt",
    "LIDL": "supermarkt",
    "ALDI": "supermarkt",
    "GALL & GALL": "dranken",
    "HEINEKEN": "dranken",
    "COCA-COLA": "dranken",
    "VRUMONA": "dranken",
    "THUISBEZORGD": "bezorgplatform",
    "UBER EATS": "bezorgplatform",
    "DELIVEROO": "deliveroo",
}

# Kostenposten voor horeca boekhouding
EXPENSE_CATEGORIES = {
    "inkoop_food": "Inkoop voedsel/ingrediënten",
    "inkoop_dranken_laag": "Inkoop dranken (9% BTW)",
    "inkoop_dranken_hoog": "Inkoop dranken alcohol (21% BTW)",
    "verpakking": "Verpakkingsmateriaal",
    "schoonmaak": "Schoonmaakmiddelen",
    "apparatuur": "Apparatuur & inventaris",
    "onderhoud": "Onderhoud & reparatie",
    "marketing": "Marketing & reclame",
    "kantoor": "Kantoorartikelen",
    "bezorgkosten": "Bezorgkosten/commissie",
    "overig": "Overige kosten",
}


# ============================================
# TEST MODUS - Horeca fake data
# ============================================

def generate_mock_receipt_horeca() -> dict:
    """Genereer fake horeca bonnetje data voor testen."""
    suppliers = [
        ("Sligro", "groothandel"),
        ("Makro", "groothandel"),
        ("Hanos", "groothandel"),
        ("Albert Heijn", "supermarkt"),
        ("Gall & Gall", "dranken"),
    ]

    store_name, supplier_type = random.choice(suppliers)

    # Random datum in de afgelopen 30 dagen
    days_ago = random.randint(0, 30)
    date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # Horeca specifieke items met BTW tarief
    possible_items = {
        "groothandel": [
            ("Kipfilet 5kg", 42.50, 9, "inkoop_food"),
            ("Frietaardappelen 10kg", 12.99, 9, "inkoop_food"),
            ("Mozzarella 2kg", 18.75, 9, "inkoop_food"),
            ("Tomatensaus 3L", 8.99, 9, "inkoop_food"),
            ("Cola 24x33cl", 14.99, 9, "inkoop_dranken_laag"),
            ("Heineken 24x30cl", 24.99, 21, "inkoop_dranken_hoog"),
            ("Wijn Huismerk 6x75cl", 35.94, 21, "inkoop_dranken_hoog"),
            ("Servettten 1000st", 12.50, 21, "verpakking"),
            ("Aluminium bakjes 100st", 18.99, 21, "verpakking"),
            ("Afwasmiddel 5L", 14.99, 21, "schoonmaak"),
        ],
        "supermarkt": [
            ("Melk 12x1L", 15.48, 9, "inkoop_food"),
            ("Boter 500g", 4.99, 9, "inkoop_food"),
            ("Eieren 30st", 8.99, 9, "inkoop_food"),
            ("Suiker 5kg", 6.99, 9, "inkoop_food"),
        ],
        "dranken": [
            ("Wodka 1L", 18.99, 21, "inkoop_dranken_hoog"),
            ("Gin 70cl", 24.99, 21, "inkoop_dranken_hoog"),
            ("Rum 1L", 19.99, 21, "inkoop_dranken_hoog"),
            ("Whisky 70cl", 29.99, 21, "inkoop_dranken_hoog"),
            ("Aperol 70cl", 16.99, 21, "inkoop_dranken_hoog"),
        ],
    }

    items_pool = possible_items.get(supplier_type, possible_items["groothandel"])
    num_items = random.randint(3, min(8, len(items_pool)))
    selected_items = random.sample(items_pool, num_items)

    items = []
    btw_9_total = 0
    btw_21_total = 0

    for desc, price, btw_pct, expense_cat in selected_items:
        qty = random.randint(1, 3)
        total_price = round(price * qty, 2)

        # Bereken BTW
        if btw_pct == 9:
            btw_amount = round(total_price * 0.09 / 1.09, 2)
            btw_9_total += btw_amount
        else:
            btw_amount = round(total_price * 0.21 / 1.21, 2)
            btw_21_total += btw_amount

        items.append({
            "description": desc,
            "quantity": qty,
            "unit_price": price,
            "total_price": total_price,
            "btw_percentage": btw_pct,
            "btw_amount": btw_amount,
            "expense_category": expense_cat,
        })

    total = sum(item["total_price"] for item in items)
    total_excl_btw = round(total - btw_9_total - btw_21_total, 2)

    payment_method = random.choice(["pin", "pin", "factuur", "factuur"])

    return {
        "store_name": store_name,
        "supplier_type": supplier_type,
        "date": date,
        "invoice_number": f"INV-{random.randint(100000, 999999)}",
        "total_amount": round(total, 2),
        "total_excl_btw": total_excl_btw,
        "btw_9_amount": round(btw_9_total, 2),
        "btw_21_amount": round(btw_21_total, 2),
        "btw_amount": round(btw_9_total + btw_21_total, 2),
        "payment_method": payment_method,
        "category": supplier_type,
        "items": items,
        "raw_text": f"[TEST MODUS] {store_name} - Fake horeca bonnetje",
        "test_mode": True,
        # Samenvatting per kostenpost
        "expense_summary": calculate_expense_summary(items),
    }


def calculate_expense_summary(items: list) -> dict:
    """Bereken totalen per kostenpost."""
    summary = {}
    for item in items:
        cat = item.get("expense_category", "overig")
        if cat not in summary:
            summary[cat] = {"amount": 0, "btw": 0, "count": 0}
        summary[cat]["amount"] += item.get("total_price", 0)
        summary[cat]["btw"] += item.get("btw_amount", 0)
        summary[cat]["count"] += 1

    # Round values
    for cat in summary:
        summary[cat]["amount"] = round(summary[cat]["amount"], 2)
        summary[cat]["btw"] = round(summary[cat]["btw"], 2)

    return summary


async def analyze_receipt_mock(image_path: str) -> dict:
    """Test modus: genereer fake horeca data zonder API calls."""
    return generate_mock_receipt_horeca()


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
        "supplier_type": None,
        "date": None,
        "invoice_number": None,
        "total_amount": None,
        "total_excl_btw": None,
        "btw_9_amount": None,
        "btw_21_amount": None,
        "btw_amount": None,
        "payment_method": "onbekend",
        "category": "overig",
        "items": [],
        "expense_summary": {}
    }

    text_upper = text.upper()

    # Horeca leveranciers detectie
    for supplier_key, supplier_type in HORECA_SUPPLIERS.items():
        if supplier_key in text_upper:
            result["store_name"] = supplier_key.title()
            result["supplier_type"] = supplier_type
            result["category"] = supplier_type
            break

    # Factuurnummer detectie
    invoice_patterns = [
        r'FACTUUR(?:NUMMER)?[:\s#]*([A-Z0-9-]+)',
        r'INVOICE[:\s#]*([A-Z0-9-]+)',
        r'BON(?:NUMMER)?[:\s#]*(\d+)',
    ]
    for pattern in invoice_patterns:
        match = re.search(pattern, text_upper)
        if match:
            result["invoice_number"] = match.group(1)
            break

    # Datum detectie
    date_patterns = [
        r'(\d{2}[-/]\d{2}[-/]\d{4})',
        r'(\d{4}[-/]\d{2}[-/]\d{2})',
        r'(\d{2}[-/]\d{2}[-/]\d{2})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
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
    ]
    for pattern in total_patterns:
        match = re.search(pattern, text_upper)
        if match:
            result["total_amount"] = float(match.group(1).replace(',', '.'))
            break

    # BTW 9% detectie
    btw9_patterns = [
        r'BTW\s*9%?[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'9%\s*BTW[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'LAAG[:\s]*[€]?\s*(\d+[.,]\d{2})',
    ]
    for pattern in btw9_patterns:
        match = re.search(pattern, text_upper)
        if match:
            result["btw_9_amount"] = float(match.group(1).replace(',', '.'))
            break

    # BTW 21% detectie
    btw21_patterns = [
        r'BTW\s*21%?[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'21%\s*BTW[:\s]*[€]?\s*(\d+[.,]\d{2})',
        r'HOOG[:\s]*[€]?\s*(\d+[.,]\d{2})',
    ]
    for pattern in btw21_patterns:
        match = re.search(pattern, text_upper)
        if match:
            result["btw_21_amount"] = float(match.group(1).replace(',', '.'))
            break

    # Totaal BTW
    if result["btw_9_amount"] or result["btw_21_amount"]:
        result["btw_amount"] = round(
            (result["btw_9_amount"] or 0) + (result["btw_21_amount"] or 0), 2
        )

    # Betaalmethode detectie
    if any(x in text_upper for x in ['PIN', 'MAESTRO', 'VISA', 'MASTERCARD', 'DEBIT']):
        result["payment_method"] = "pin"
    elif any(x in text_upper for x in ['CONTANT', 'CASH']):
        result["payment_method"] = "cash"
    elif any(x in text_upper for x in ['FACTUUR', 'OP REKENING', 'CREDIT']):
        result["payment_method"] = "factuur"

    return result


# ============================================
# OPENAI VISION - Horeca optimized
# ============================================

async def analyze_receipt_openai(image_path: str, api_key: str) -> dict:
    """
    Analyseer een bonnetje/factuur voor horeca boekhouding met OpenAI Vision.
    Geoptimaliseerd voor Nederlandse horeca BTW-administratie.
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    suffix = Path(image_path).suffix.lower()
    media_type = "image/jpeg"
    if suffix == ".png":
        media_type = "image/png"
    elif suffix == ".webp":
        media_type = "image/webp"

    prompt = """Analyseer dit bonnetje/factuur voor HORECA BOEKHOUDING en extraheer de informatie in JSON formaat.

Dit is voor een horecazaak in Amsterdam. Let specifiek op BTW-uitsplitsing en kostenposten.

{
    "store_name": "naam leverancier/winkel",
    "supplier_type": "groothandel" of "supermarkt" of "dranken" of "bezorgplatform" of "overig",
    "date": "YYYY-MM-DD",
    "invoice_number": "factuurnummer indien zichtbaar",

    "total_amount": getal (totaal INCLUSIEF BTW),
    "total_excl_btw": getal (totaal EXCLUSIEF BTW indien zichtbaar),

    "btw_9_amount": getal (BTW 9% laag tarief - voedsel, non-alcoholische dranken),
    "btw_21_amount": getal (BTW 21% hoog tarief - alcohol, non-food items),
    "btw_amount": getal (totaal BTW),

    "payment_method": "pin" of "cash" of "factuur" of "onbekend",
    "category": "groothandel" of "supermarkt" of "dranken" of "verpakking" of "schoonmaak" of "overig",

    "items": [
        {
            "description": "productnaam",
            "quantity": aantal,
            "unit_price": prijs per stuk,
            "total_price": totaalprijs incl BTW,
            "btw_percentage": 9 of 21,
            "btw_amount": BTW bedrag voor dit item,
            "expense_category": "inkoop_food" of "inkoop_dranken_laag" of "inkoop_dranken_hoog" of "verpakking" of "schoonmaak" of "apparatuur" of "overig"
        }
    ],

    "expense_summary": {
        "inkoop_food": {"amount": totaal, "btw": btw_totaal},
        "inkoop_dranken_laag": {"amount": totaal, "btw": btw_totaal},
        "inkoop_dranken_hoog": {"amount": totaal, "btw": btw_totaal},
        ...
    },

    "raw_text": "alle leesbare tekst"
}

BELANGRIJK voor expense_category:
- inkoop_food: Alle eten/ingrediënten (9% BTW)
- inkoop_dranken_laag: Non-alcoholische dranken (9% BTW)
- inkoop_dranken_hoog: Alcoholische dranken (21% BTW)
- verpakking: Bakjes, servetten, tasjes (21% BTW)
- schoonmaak: Schoonmaakmiddelen (21% BTW)
- apparatuur: Keukenapparatuur, inventaris (21% BTW)

BELANGRIJK voor BTW:
- 9% BTW: Voedsel, non-alcoholische dranken
- 21% BTW: Alcohol, non-food items, verpakking, schoonmaak

Bekende horeca leveranciers: Sligro, Makro, Hanos, Bidfood, Deli XL

Geef ALLEEN valide JSON terug, geen andere tekst."""

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
        max_tokens=3000
    )

    content = response.choices[0].message.content.strip()

    # Verwijder markdown code blocks
    if content.startswith("```"):
        content = re.sub(r"^```json?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

    try:
        result = json.loads(content)
        # Bereken expense_summary als niet aanwezig
        if not result.get("expense_summary") and result.get("items"):
            result["expense_summary"] = calculate_expense_summary(result["items"])
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
# HOOFDFUNCTIE
# ============================================

async def analyze_receipt(image_path: str, api_key: str = None, mode: str = "auto") -> dict:
    """
    Analyseer een bonnetje met de gekozen methode.

    Modes:
    - "test": Fake horeca data, geen API calls
    - "tesseract": Gratis lokale OCR
    - "openai": OpenAI Vision API (beste kwaliteit)
    - "auto": OpenAI als key beschikbaar, anders tesseract
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

    if data.get("test_mode"):
        lines.append("🧪 *TEST MODUS - Fake Data*\n")
    else:
        lines.append("📋 *Bonnetje Verwerkt*\n")

    if data.get("store_name"):
        lines.append(f"🏪 *Leverancier:* {data['store_name']}")

    if data.get("supplier_type"):
        lines.append(f"🏷️ *Type:* {data['supplier_type'].capitalize()}")

    if data.get("date"):
        lines.append(f"📅 *Datum:* {data['date']}")

    if data.get("invoice_number"):
        lines.append(f"📄 *Factuurnr:* {data['invoice_number']}")

    # Bedragen
    lines.append("")
    if data.get("total_amount") is not None:
        lines.append(f"💰 *Totaal incl BTW:* €{data['total_amount']:.2f}")

    if data.get("total_excl_btw") is not None:
        lines.append(f"💵 *Totaal excl BTW:* €{data['total_excl_btw']:.2f}")

    # BTW uitsplitsing
    if data.get("btw_9_amount") is not None or data.get("btw_21_amount") is not None:
        lines.append("")
        lines.append("📊 *BTW Uitsplitsing:*")
        if data.get("btw_9_amount"):
            lines.append(f"  • 9% (laag): €{data['btw_9_amount']:.2f}")
        if data.get("btw_21_amount"):
            lines.append(f"  • 21% (hoog): €{data['btw_21_amount']:.2f}")
        if data.get("btw_amount"):
            lines.append(f"  • *Totaal BTW:* €{data['btw_amount']:.2f}")

    # Betaalmethode
    if data.get("payment_method"):
        emoji = {"pin": "💳", "cash": "💵", "factuur": "📄", "onbekend": "❓"}
        lines.append(f"\n{emoji.get(data['payment_method'], '❓')} *Betaling:* {data['payment_method'].upper()}")

    # Kostenposten samenvatting
    expense_summary = data.get("expense_summary", {})
    if expense_summary:
        lines.append("\n📂 *Per Kostenpost:*")
        for cat, values in expense_summary.items():
            cat_name = EXPENSE_CATEGORIES.get(cat, cat)
            amount = values.get("amount", 0)
            if amount > 0:
                lines.append(f"  • {cat_name}: €{amount:.2f}")

    # Items (max 5)
    items = data.get("items", [])
    if items:
        lines.append("\n📝 *Producten:*")
        for item in items[:5]:
            desc = item.get("description", "Onbekend")
            price = item.get("total_price")
            btw = item.get("btw_percentage", "?")
            if price is not None:
                lines.append(f"  • {desc}: €{price:.2f} ({btw}%)")
            else:
                lines.append(f"  • {desc}")
        if len(items) > 5:
            lines.append(f"  _...en {len(items) - 5} meer items_")

    if data.get("error"):
        lines.append(f"\n⚠️ _{data['error']}_")

    return "\n".join(lines)
