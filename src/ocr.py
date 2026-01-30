import base64
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI


async def analyze_receipt(image_path: str, api_key: str) -> dict:
    """
    Analyseer een bonnetje foto met OpenAI Vision.
    Extraheert: winkel, datum, totaal, BTW, betaalmethode, items.
    """
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
        # Als JSON parsing faalt, return basis structuur
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


def format_receipt_summary(data: dict) -> str:
    """Formatteer de bonnetje data als leesbare tekst voor Telegram."""
    lines = ["📋 *Bonnetje Verwerkt*\n"]

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
        for item in items[:10]:  # Max 10 items tonen
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
