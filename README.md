# Bonnetjes Bot 🧾

Een Telegram bot die bonnetjes scant met AI (OpenAI Vision) en automatisch overzichten maakt in Excel.

## Features

- 📸 **Foto's van bonnetjes** sturen via Telegram
- 🤖 **AI-powered OCR** met OpenAI Vision (GPT-4o)
- 📊 **Automatische extractie** van:
  - Winkelnaam
  - Datum
  - Totaalbedrag
  - BTW
  - Betaalmethode (PIN/Cash/Onbekend)
  - Categorie (supermarkt, restaurant, etc.)
  - Individuele producten
- 📈 **Maandoverzichten** direct in Telegram
- 📁 **Excel exports** met:
  - Alle bonnetjes
  - Overzicht per categorie
  - Overzicht per betaalmethode

## Installatie

### 1. Clone de repository

```bash
git clone <repository-url>
cd CloudClaude
```

### 2. Maak een virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# of
venv\Scripts\activate  # Windows
```

### 3. Installeer dependencies

```bash
pip install -r requirements.txt
```

### 4. Configureer de bot

Kopieer `.env.example` naar `.env` en vul de waarden in:

```bash
cp .env.example .env
```

Je hebt nodig:

#### Telegram Bot Token
1. Open Telegram en zoek naar `@BotFather`
2. Stuur `/newbot` en volg de instructies
3. Kopieer de token naar `.env`

#### OpenAI API Key
1. Ga naar [platform.openai.com](https://platform.openai.com)
2. Maak een API key aan
3. Kopieer de key naar `.env`

### 5. Start de bot

```bash
python main.py
```

## Gebruik

### Commando's

| Commando | Beschrijving |
|----------|--------------|
| `/start` | Welkomstbericht |
| `/help` | Hulp en instructies |
| `/overzicht` | Maandoverzicht van huidige maand |
| `/overzicht 2024 1` | Overzicht van januari 2024 |
| `/export` | Excel export van huidige maand |
| `/export 2024 1` | Export van januari 2024 |

### Bonnetje toevoegen

Stuur simpelweg een foto van je bonnetje naar de bot. De bot zal automatisch:
1. Het bonnetje scannen met AI
2. Alle gegevens extraheren
3. Opslaan in de database
4. Een samenvatting terugsturen

### Tips voor goede scans

- Zorg voor goede belichting
- Houd de camera recht boven het bonnetje
- Zorg dat alle tekst leesbaar is
- Vermijd schaduwen en kreukels

## Project Structuur

```
CloudClaude/
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Voorbeeld configuratie
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── bot.py           # Telegram bot handlers
│   ├── database.py      # SQLite database
│   ├── ocr.py           # OpenAI Vision OCR
│   └── excel_export.py  # Excel rapport generator
├── exports/             # Gegenereerde Excel bestanden
└── images/              # Opgeslagen bonnetje foto's
```

## Database

De bot gebruikt SQLite voor lokale opslag. De database wordt automatisch aangemaakt bij de eerste start.

### Tabellen

- `receipts` - Bonnetje metadata
- `receipt_items` - Individuele producten per bonnetje

## Kosten

- **Telegram**: Gratis
- **OpenAI API**: ~$0.01-0.03 per bonnetje (afhankelijk van grootte)

## Licentie

MIT
