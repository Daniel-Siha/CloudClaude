# Bonnetjes Bot

Een Telegram bot die bonnetjes scant en automatisch overzichten maakt in Excel.

## Features

- Foto's van bonnetjes sturen via Telegram
- Meerdere OCR opties (gratis en betaald)
- Automatische extractie van:
  - Winkelnaam
  - Datum
  - Totaalbedrag
  - BTW
  - Betaalmethode (PIN/Cash/Onbekend)
  - Categorie (supermarkt, restaurant, etc.)
  - Individuele producten
- Maandoverzichten direct in Telegram
- Excel exports met alle details

## OCR Modi

| Modus | Kosten | Kwaliteit | Beschrijving |
|-------|--------|-----------|--------------|
| `test` | Gratis | N/A | Fake data voor development/testen |
| `tesseract` | Gratis | Matig | Lokale OCR, vereist Tesseract installatie |
| `openai` | ~€0.01-0.03/bon | Excellent | OpenAI Vision API (GPT-4o) |
| `auto` | Varieert | Varieert | OpenAI als key aanwezig, anders Tesseract |

**Aanbeveling**: Start met `OCR_MODE=test` om de bot te testen zonder kosten!

## Quick Start

```bash
# 1. Clone & setup
git clone <repository-url>
cd CloudClaude
python -m venv venv
source venv/bin/activate

# 2. Installeer dependencies
pip install -r requirements.txt

# 3. Configureer
cp .env.example .env
# Edit .env met je Telegram token

# 4. Start (test modus)
python main.py
```

## Configuratie

### Telegram Bot Token (verplicht)
1. Open Telegram en zoek `@BotFather`
2. Stuur `/newbot` en volg de instructies
3. Kopieer de token naar `.env`

### OCR Modus kiezen

In je `.env` bestand:

```bash
# Voor testen (fake data, gratis)
OCR_MODE=test

# Voor gratis OCR (vereist Tesseract)
OCR_MODE=tesseract

# Voor beste kwaliteit (kost geld)
OCR_MODE=openai
OPENAI_API_KEY=sk-...
```

### Tesseract installeren (optioneel)

Alleen nodig als je `OCR_MODE=tesseract` gebruikt:

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-nld

# macOS
brew install tesseract tesseract-lang

# Windows
# Download van: https://github.com/UB-Mannheim/tesseract/wiki
```

## Commando's

| Commando | Beschrijving |
|----------|--------------|
| `/start` | Welkomstbericht |
| `/help` | Hulp en instructies |
| `/overzicht` | Maandoverzicht van huidige maand |
| `/overzicht 2024 1` | Overzicht van januari 2024 |
| `/export` | Excel export van huidige maand |
| `/export 2024 1` | Export van januari 2024 |

## Project Structuur

```
CloudClaude/
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Voorbeeld configuratie
├── src/
│   ├── bot.py           # Telegram bot handlers
│   ├── database.py      # SQLite database
│   ├── ocr.py           # OCR modules (test/tesseract/openai)
│   └── excel_export.py  # Excel rapport generator
├── exports/             # Gegenereerde Excel bestanden
└── images/              # Opgeslagen bonnetje foto's
```

## Licentie

MIT
