import os
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from .database import init_db, save_receipt, save_receipt_items, get_monthly_summary
from .ocr import analyze_receipt, format_receipt_summary
from .excel_export import create_monthly_report

# Laad environment variables
load_dotenv()

# Logging configuratie
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Paths
IMAGES_PATH = Path(__file__).parent.parent / "images"
IMAGES_PATH.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start commando - welkomstbericht."""
    welcome_text = """
👋 *Welkom bij de Bonnetjes Bot!*

Stuur mij een foto van je bonnetje en ik zal het automatisch verwerken.

*Beschikbare commando's:*
📸 Stuur een foto → Bonnetje wordt gescand en opgeslagen
/overzicht → Bekijk je maandoverzicht
/export → Download Excel rapport
/help → Hulp en instructies

_Tip: Maak duidelijke foto's voor de beste resultaten!_
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help commando."""
    help_text = """
📖 *Hoe gebruik je deze bot?*

*1. Bonnetje toevoegen:*
Stuur simpelweg een foto van je bonnetje. De bot herkent automatisch:
• Winkelnaam
• Datum
• Totaalbedrag
• BTW
• Betaalmethode (PIN/Cash)
• Producten

*2. Overzicht bekijken:*
Gebruik /overzicht om een samenvatting te zien van je uitgaven deze maand.

*3. Excel exporteren:*
Gebruik /export om een gedetailleerd Excel bestand te krijgen met:
• Alle bonnetjes
• Overzicht per categorie
• Overzicht per betaalmethode

*Tips voor goede scans:*
• Zorg voor goede belichting
• Houd de camera recht boven het bonnetje
• Zorg dat alle tekst leesbaar is
• Vermijd schaduwen

_Problemen? Stuur een nieuwe, duidelijkere foto!_
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verwerk een foto van een bonnetje."""
    user_id = update.effective_user.id

    # Haal OCR modus op
    ocr_mode = os.getenv("OCR_MODE", "test").lower()

    # Stuur bezig bericht
    mode_text = {
        "test": "🧪 TEST MODUS",
        "tesseract": "🔍 Tesseract OCR",
        "openai": "🤖 OpenAI Vision",
        "auto": "🔍 Auto"
    }
    processing_msg = await update.message.reply_text(
        f"_{mode_text.get(ocr_mode, 'Bonnetje')} wordt verwerkt..._",
        parse_mode='Markdown'
    )

    try:
        # Download de foto (grootste versie)
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # Sla de foto lokaal op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{user_id}_{timestamp}.jpg"
        image_path = IMAGES_PATH / image_filename
        await file.download_to_drive(image_path)

        # Analyseer met OCR
        openai_key = os.getenv("OPENAI_API_KEY")

        # Check of OpenAI key nodig is
        if ocr_mode == "openai" and not openai_key:
            await processing_msg.edit_text(
                "❌ OpenAI API key niet geconfigureerd maar OCR_MODE=openai.\n"
                "Zet OCR_MODE=test of OCR_MODE=tesseract in je .env bestand."
            )
            return

        result = await analyze_receipt(str(image_path), openai_key, mode=ocr_mode)

        # Sla op in database
        receipt_id = await save_receipt(
            telegram_user_id=user_id,
            store_name=result.get('store_name'),
            date=result.get('date'),
            total_amount=result.get('total_amount'),
            btw_amount=result.get('btw_amount'),
            payment_method=result.get('payment_method'),
            category=result.get('category'),
            raw_text=result.get('raw_text'),
            image_path=str(image_path)
        )

        # Sla items op
        if result.get('items'):
            await save_receipt_items(receipt_id, result['items'])

        # Formatteer en stuur resultaat
        summary = format_receipt_summary(result)
        summary += f"\n\n✅ _Opgeslagen als bonnetje #{receipt_id}_"

        await processing_msg.edit_text(summary, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        await processing_msg.edit_text(
            f"❌ Er ging iets mis bij het verwerken van het bonnetje.\n"
            f"_Probeer een duidelijkere foto te maken._"
        )


async def overview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toon maandoverzicht."""
    user_id = update.effective_user.id
    now = datetime.now()

    # Check of er argumenten zijn (bijv. /overzicht 2024 1)
    args = context.args
    if len(args) >= 2:
        try:
            year = int(args[0])
            month = int(args[1])
        except ValueError:
            year, month = now.year, now.month
    else:
        year, month = now.year, now.month

    summary = await get_monthly_summary(user_id, year, month)

    if not summary or summary.get('total_receipts', 0) == 0:
        await update.message.reply_text(
            f"📭 Geen bonnetjes gevonden voor {month:02d}/{year}.\n"
            f"_Stuur een foto om te beginnen!_",
            parse_mode='Markdown'
        )
        return

    # Formatteer overzicht
    text = f"""
📊 *Overzicht {month:02d}/{year}*

📋 Aantal bonnetjes: *{summary.get('total_receipts', 0)}*

💰 *Totalen:*
├ Totaal uitgegeven: €{summary.get('total_spent', 0) or 0:.2f}
├ Totaal BTW: €{summary.get('total_btw', 0) or 0:.2f}
│
├ 💳 PIN: €{summary.get('total_pin', 0) or 0:.2f}
├ 💵 Cash: €{summary.get('total_cash', 0) or 0:.2f}
└ ❓ Onbekend: €{summary.get('total_unknown', 0) or 0:.2f}

_Gebruik /export voor een gedetailleerd Excel bestand._
"""

    # Voeg navigatie knoppen toe
    keyboard = [
        [
            InlineKeyboardButton("◀️ Vorige maand", callback_data=f"overview_{year}_{month-1}"),
            InlineKeyboardButton("Volgende maand ▶️", callback_data=f"overview_{year}_{month+1}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)


async def overview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle overview navigation callbacks."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    _, year, month = query.data.split('_')
    year, month = int(year), int(month)

    # Handle month overflow
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    summary = await get_monthly_summary(user_id, year, month)

    if not summary or summary.get('total_receipts', 0) == 0:
        text = f"📭 Geen bonnetjes gevonden voor {month:02d}/{year}."
    else:
        text = f"""
📊 *Overzicht {month:02d}/{year}*

📋 Aantal bonnetjes: *{summary.get('total_receipts', 0)}*

💰 *Totalen:*
├ Totaal uitgegeven: €{summary.get('total_spent', 0) or 0:.2f}
├ Totaal BTW: €{summary.get('total_btw', 0) or 0:.2f}
│
├ 💳 PIN: €{summary.get('total_pin', 0) or 0:.2f}
├ 💵 Cash: €{summary.get('total_cash', 0) or 0:.2f}
└ ❓ Onbekend: €{summary.get('total_unknown', 0) or 0:.2f}
"""

    keyboard = [
        [
            InlineKeyboardButton("◀️ Vorige maand", callback_data=f"overview_{year}_{month-1}"),
            InlineKeyboardButton("Volgende maand ▶️", callback_data=f"overview_{year}_{month+1}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exporteer bonnetjes naar Excel."""
    user_id = update.effective_user.id
    now = datetime.now()

    # Check argumenten
    args = context.args
    if len(args) >= 2:
        try:
            year = int(args[0])
            month = int(args[1])
        except ValueError:
            year, month = now.year, now.month
    else:
        year, month = now.year, now.month

    await update.message.reply_text(
        f"📝 _Excel rapport wordt gemaakt voor {month:02d}/{year}..._",
        parse_mode='Markdown'
    )

    try:
        filepath = await create_monthly_report(user_id, year, month)

        if filepath:
            await update.message.reply_document(
                document=open(filepath, 'rb'),
                filename=f"bonnetjes_{year}_{month:02d}.xlsx",
                caption=f"📊 Bonnetjes overzicht voor {month:02d}/{year}"
            )
        else:
            await update.message.reply_text(
                f"📭 Geen bonnetjes gevonden voor {month:02d}/{year}.",
                parse_mode='Markdown'
            )

    except Exception as e:
        logger.error(f"Error creating export: {e}")
        await update.message.reply_text(
            "❌ Er ging iets mis bij het maken van het rapport."
        )


def main():
    """Start de bot."""
    # Haal token op
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN niet gevonden in .env bestand!")
        print("Maak een .env bestand aan met je Telegram bot token.")
        return

    # Initialiseer database
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())

    # Maak application
    application = Application.builder().token(token).build()

    # Voeg handlers toe
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("overzicht", overview))
    application.add_handler(CommandHandler("export", export))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CallbackQueryHandler(overview_callback, pattern=r"^overview_"))

    # Start de bot
    ocr_mode = os.getenv("OCR_MODE", "test").lower()
    mode_names = {
        "test": "TEST MODUS (fake data)",
        "tesseract": "Tesseract OCR (gratis)",
        "openai": "OpenAI Vision (betaald)",
        "auto": "Auto (OpenAI als key aanwezig, anders Tesseract)"
    }
    print("🤖 Bonnetjes Bot is gestart!")
    print(f"📋 OCR Modus: {mode_names.get(ocr_mode, ocr_mode)}")
    print("Druk op Ctrl+C om te stoppen.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
