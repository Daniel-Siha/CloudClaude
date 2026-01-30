import os
import json
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
    ConversationHandler,
    ContextTypes,
    filters,
)

from .database import (
    init_db, save_receipt, save_receipt_items, get_monthly_summary,
    update_receipt, delete_receipt
)
from .ocr import analyze_receipt, format_receipt_summary, EXPENSE_CATEGORIES
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

# Conversation states voor edits
EDIT_STORE, EDIT_AMOUNT, EDIT_BTW, EDIT_PAYMENT = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start commando - welkomstbericht."""
    welcome_text = """
👋 *Welkom bij de Bonnetjes Bot!*

Stuur mij een foto van je bonnetje en ik zal het automatisch verwerken.

*Beschikbare commando's:*
📸 Stuur een foto → Bonnetje wordt gescand
/overzicht → Bekijk je maandoverzicht
/export → Download Excel rapport
/help → Hulp en instructies

_Na het scannen kun je de info direct bevestigen of aanpassen!_
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help commando."""
    help_text = """
📖 *Hoe gebruik je deze bot?*

*1. Bonnetje scannen:*
Stuur een foto → Bot scant automatisch → Bevestig of pas aan

*2. Wat wordt herkend:*
• Leverancier (Sligro, Makro, etc.)
• Datum & factuurnummer
• Totaal incl/excl BTW
• BTW 9% en 21% apart
• Betaalmethode
• Alle producten

*3. Na het scannen:*
✅ Klopt? → Bevestigen
✏️ Fout? → Aanpassen via knoppen

*4. Overzichten:*
/overzicht → Maandsamenvatting
/export → Excel download

_Tip: Duidelijke foto's geven betere resultaten!_
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
        # Download de foto
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # Sla de foto lokaal op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{user_id}_{timestamp}.jpg"
        image_path = IMAGES_PATH / image_filename
        await file.download_to_drive(image_path)

        # Analyseer met OCR
        openai_key = os.getenv("OPENAI_API_KEY")

        if ocr_mode == "openai" and not openai_key:
            await processing_msg.edit_text(
                "❌ OpenAI API key niet geconfigureerd.\n"
                "Zet OCR_MODE=test in je .env bestand."
            )
            return

        result = await analyze_receipt(str(image_path), openai_key, mode=ocr_mode)

        # Sla TIJDELIJK op in context (nog niet in database)
        # Pas opslaan na bevestiging
        context.user_data['pending_receipt'] = {
            'result': result,
            'image_path': str(image_path)
        }

        # Formatteer resultaat
        summary = format_receipt_summary(result)

        # Voeg bevestig/aanpas knoppen toe
        keyboard = [
            [
                InlineKeyboardButton("✅ Correct, opslaan", callback_data="receipt_confirm"),
                InlineKeyboardButton("❌ Annuleren", callback_data="receipt_cancel"),
            ],
            [
                InlineKeyboardButton("✏️ Winkel", callback_data="receipt_edit_store"),
                InlineKeyboardButton("✏️ Bedrag", callback_data="receipt_edit_amount"),
            ],
            [
                InlineKeyboardButton("✏️ BTW", callback_data="receipt_edit_btw"),
                InlineKeyboardButton("✏️ Betaling", callback_data="receipt_edit_payment"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        summary += "\n\n⬇️ *Klopt dit? Bevestig of pas aan:*"

        await processing_msg.edit_text(summary, parse_mode='Markdown', reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        await processing_msg.edit_text(
            f"❌ Er ging iets mis bij het verwerken.\n_Probeer een duidelijkere foto._"
        )


async def receipt_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bevestig en sla het bonnetje op."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    pending = context.user_data.get('pending_receipt')

    if not pending:
        await query.edit_message_text("❌ Geen bonnetje om op te slaan. Stuur een nieuwe foto.")
        return

    result = pending['result']
    image_path = pending['image_path']

    # Nu opslaan in database
    receipt_id = await save_receipt(
        telegram_user_id=user_id,
        store_name=result.get('store_name'),
        supplier_type=result.get('supplier_type'),
        date=result.get('date'),
        invoice_number=result.get('invoice_number'),
        total_amount=result.get('total_amount'),
        total_excl_btw=result.get('total_excl_btw'),
        btw_amount=result.get('btw_amount'),
        btw_9_amount=result.get('btw_9_amount'),
        btw_21_amount=result.get('btw_21_amount'),
        payment_method=result.get('payment_method'),
        category=result.get('category'),
        raw_text=result.get('raw_text'),
        image_path=image_path
    )

    # Sla items op
    if result.get('items'):
        await save_receipt_items(receipt_id, result['items'])

    # Clear pending
    context.user_data.pop('pending_receipt', None)

    # Update bericht
    summary = format_receipt_summary(result)
    summary += f"\n\n✅ *Opgeslagen als bonnetje #{receipt_id}*"

    await query.edit_message_text(summary, parse_mode='Markdown')


async def receipt_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Annuleer het bonnetje."""
    query = update.callback_query
    await query.answer()

    # Clear pending
    context.user_data.pop('pending_receipt', None)

    await query.edit_message_text("❌ Bonnetje geannuleerd. Stuur een nieuwe foto om opnieuw te beginnen.")


async def receipt_edit_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start edit voor winkelnaam."""
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get('pending_receipt')
    if not pending:
        await query.edit_message_text("❌ Geen bonnetje om aan te passen.")
        return ConversationHandler.END

    current = pending['result'].get('store_name', 'Onbekend')

    await query.edit_message_text(
        f"✏️ *Winkelnaam aanpassen*\n\n"
        f"Huidige waarde: `{current}`\n\n"
        f"Typ de nieuwe winkelnaam of /cancel om te annuleren:",
        parse_mode='Markdown'
    )

    return EDIT_STORE


async def save_edit_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sla de nieuwe winkelnaam op."""
    new_value = update.message.text.strip()

    pending = context.user_data.get('pending_receipt')
    if pending:
        pending['result']['store_name'] = new_value

    await update.message.reply_text(f"✅ Winkelnaam aangepast naar: *{new_value}*", parse_mode='Markdown')

    # Toon opnieuw de bevestig knoppen
    await show_pending_receipt(update, context)

    return ConversationHandler.END


async def receipt_edit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start edit voor bedrag."""
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get('pending_receipt')
    if not pending:
        await query.edit_message_text("❌ Geen bonnetje om aan te passen.")
        return ConversationHandler.END

    current = pending['result'].get('total_amount', 0)

    await query.edit_message_text(
        f"✏️ *Totaalbedrag aanpassen*\n\n"
        f"Huidige waarde: `€{current:.2f}`\n\n"
        f"Typ het nieuwe bedrag (bijv. `125.50`) of /cancel:",
        parse_mode='Markdown'
    )

    return EDIT_AMOUNT


async def save_edit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sla het nieuwe bedrag op."""
    try:
        new_value = float(update.message.text.strip().replace(',', '.').replace('€', ''))
    except ValueError:
        await update.message.reply_text("❌ Ongeldig bedrag. Probeer opnieuw (bijv. `125.50`):")
        return EDIT_AMOUNT

    pending = context.user_data.get('pending_receipt')
    if pending:
        pending['result']['total_amount'] = new_value

    await update.message.reply_text(f"✅ Bedrag aangepast naar: *€{new_value:.2f}*", parse_mode='Markdown')

    await show_pending_receipt(update, context)
    return ConversationHandler.END


async def receipt_edit_btw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start edit voor BTW."""
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get('pending_receipt')
    if not pending:
        await query.edit_message_text("❌ Geen bonnetje om aan te passen.")
        return ConversationHandler.END

    btw_9 = pending['result'].get('btw_9_amount', 0) or 0
    btw_21 = pending['result'].get('btw_21_amount', 0) or 0

    await query.edit_message_text(
        f"✏️ *BTW aanpassen*\n\n"
        f"Huidige waarden:\n"
        f"• 9% BTW: `€{btw_9:.2f}`\n"
        f"• 21% BTW: `€{btw_21:.2f}`\n\n"
        f"Typ beide waarden gescheiden door een spatie:\n"
        f"Bijv. `5.50 12.30` (eerst 9%, dan 21%)\n\n"
        f"Of /cancel om te annuleren:",
        parse_mode='Markdown'
    )

    return EDIT_BTW


async def save_edit_btw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sla de nieuwe BTW waarden op."""
    try:
        parts = update.message.text.strip().replace(',', '.').split()
        btw_9 = float(parts[0])
        btw_21 = float(parts[1]) if len(parts) > 1 else 0
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Ongeldige invoer. Gebruik: `5.50 12.30` (9% BTW, 21% BTW):")
        return EDIT_BTW

    pending = context.user_data.get('pending_receipt')
    if pending:
        pending['result']['btw_9_amount'] = btw_9
        pending['result']['btw_21_amount'] = btw_21
        pending['result']['btw_amount'] = btw_9 + btw_21

    await update.message.reply_text(
        f"✅ BTW aangepast:\n• 9%: €{btw_9:.2f}\n• 21%: €{btw_21:.2f}",
        parse_mode='Markdown'
    )

    await show_pending_receipt(update, context)
    return ConversationHandler.END


async def receipt_edit_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start edit voor betaalmethode."""
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get('pending_receipt')
    if not pending:
        await query.edit_message_text("❌ Geen bonnetje om aan te passen.")
        return

    current = pending['result'].get('payment_method', 'onbekend')

    # Toon knoppen voor betaalmethode
    keyboard = [
        [
            InlineKeyboardButton("💳 PIN", callback_data="payment_pin"),
            InlineKeyboardButton("💵 Cash", callback_data="payment_cash"),
        ],
        [
            InlineKeyboardButton("📄 Factuur", callback_data="payment_factuur"),
            InlineKeyboardButton("❓ Onbekend", callback_data="payment_onbekend"),
        ],
        [InlineKeyboardButton("⬅️ Terug", callback_data="payment_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"✏️ *Betaalmethode aanpassen*\n\n"
        f"Huidige waarde: `{current}`\n\n"
        f"Kies de juiste betaalmethode:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def save_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sla de nieuwe betaalmethode op."""
    query = update.callback_query
    await query.answer()

    method = query.data.replace("payment_", "")

    if method == "back":
        await show_pending_receipt_callback(update, context)
        return

    pending = context.user_data.get('pending_receipt')
    if pending:
        pending['result']['payment_method'] = method

    await query.answer(f"✅ Betaalmethode: {method.upper()}")

    await show_pending_receipt_callback(update, context)


async def show_pending_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toon het pending bonnetje opnieuw met knoppen."""
    pending = context.user_data.get('pending_receipt')
    if not pending:
        return

    result = pending['result']
    summary = format_receipt_summary(result)

    keyboard = [
        [
            InlineKeyboardButton("✅ Correct, opslaan", callback_data="receipt_confirm"),
            InlineKeyboardButton("❌ Annuleren", callback_data="receipt_cancel"),
        ],
        [
            InlineKeyboardButton("✏️ Winkel", callback_data="receipt_edit_store"),
            InlineKeyboardButton("✏️ Bedrag", callback_data="receipt_edit_amount"),
        ],
        [
            InlineKeyboardButton("✏️ BTW", callback_data="receipt_edit_btw"),
            InlineKeyboardButton("✏️ Betaling", callback_data="receipt_edit_payment"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    summary += "\n\n⬇️ *Klopt dit? Bevestig of pas aan:*"

    await update.message.reply_text(summary, parse_mode='Markdown', reply_markup=reply_markup)


async def show_pending_receipt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toon het pending bonnetje opnieuw (voor callback queries)."""
    query = update.callback_query
    pending = context.user_data.get('pending_receipt')
    if not pending:
        return

    result = pending['result']
    summary = format_receipt_summary(result)

    keyboard = [
        [
            InlineKeyboardButton("✅ Correct, opslaan", callback_data="receipt_confirm"),
            InlineKeyboardButton("❌ Annuleren", callback_data="receipt_cancel"),
        ],
        [
            InlineKeyboardButton("✏️ Winkel", callback_data="receipt_edit_store"),
            InlineKeyboardButton("✏️ Bedrag", callback_data="receipt_edit_amount"),
        ],
        [
            InlineKeyboardButton("✏️ BTW", callback_data="receipt_edit_btw"),
            InlineKeyboardButton("✏️ Betaling", callback_data="receipt_edit_payment"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    summary += "\n\n⬇️ *Klopt dit? Bevestig of pas aan:*"

    await query.edit_message_text(summary, parse_mode='Markdown', reply_markup=reply_markup)


async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Annuleer de huidige edit."""
    await update.message.reply_text("Aanpassing geannuleerd.")
    await show_pending_receipt(update, context)
    return ConversationHandler.END


async def overview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toon maandoverzicht."""
    user_id = update.effective_user.id
    now = datetime.now()

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

    text = f"""
📊 *Overzicht {month:02d}/{year}*

📋 Aantal bonnetjes: *{summary.get('total_receipts', 0)}*

💰 *Totalen:*
├ Incl BTW: €{summary.get('total_spent', 0) or 0:.2f}
├ Excl BTW: €{summary.get('total_excl_btw', 0) or 0:.2f}

📊 *BTW Uitsplitsing:*
├ 9% (laag): €{summary.get('total_btw_9', 0) or 0:.2f}
├ 21% (hoog): €{summary.get('total_btw_21', 0) or 0:.2f}
└ Totaal BTW: €{summary.get('total_btw', 0) or 0:.2f}

💳 *Per Betaalmethode:*
├ PIN: €{summary.get('total_pin', 0) or 0:.2f}
├ Cash: €{summary.get('total_cash', 0) or 0:.2f}
├ Factuur: €{summary.get('total_factuur', 0) or 0:.2f}
└ Onbekend: €{summary.get('total_unknown', 0) or 0:.2f}

_Gebruik /export voor gedetailleerd Excel rapport._
"""

    keyboard = [
        [
            InlineKeyboardButton("◀️ Vorige maand", callback_data=f"overview_{year}_{month-1}"),
            InlineKeyboardButton("Volgende maand ▶️", callback_data=f"overview_{year}_{month+1}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)


async def overview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle overview navigation."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    _, year, month = query.data.split('_')
    year, month = int(year), int(month)

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
├ Incl BTW: €{summary.get('total_spent', 0) or 0:.2f}
├ Excl BTW: €{summary.get('total_excl_btw', 0) or 0:.2f}

📊 *BTW:*
├ 9%: €{summary.get('total_btw_9', 0) or 0:.2f}
├ 21%: €{summary.get('total_btw_21', 0) or 0:.2f}
└ Totaal: €{summary.get('total_btw', 0) or 0:.2f}
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
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN niet gevonden in .env bestand!")
        return

    # Initialiseer database
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())

    # Maak application
    application = Application.builder().token(token).build()

    # Conversation handlers voor edits
    edit_store_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(receipt_edit_store, pattern="^receipt_edit_store$")],
        states={
            EDIT_STORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_edit_store)],
        },
        fallbacks=[CommandHandler("cancel", cancel_edit)],
    )

    edit_amount_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(receipt_edit_amount, pattern="^receipt_edit_amount$")],
        states={
            EDIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_edit_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel_edit)],
    )

    edit_btw_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(receipt_edit_btw, pattern="^receipt_edit_btw$")],
        states={
            EDIT_BTW: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_edit_btw)],
        },
        fallbacks=[CommandHandler("cancel", cancel_edit)],
    )

    # Voeg handlers toe
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("overzicht", overview))
    application.add_handler(CommandHandler("export", export))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Receipt callbacks
    application.add_handler(CallbackQueryHandler(receipt_confirm, pattern="^receipt_confirm$"))
    application.add_handler(CallbackQueryHandler(receipt_cancel, pattern="^receipt_cancel$"))
    application.add_handler(CallbackQueryHandler(receipt_edit_payment, pattern="^receipt_edit_payment$"))
    application.add_handler(CallbackQueryHandler(save_payment_method, pattern="^payment_"))

    # Edit handlers
    application.add_handler(edit_store_handler)
    application.add_handler(edit_amount_handler)
    application.add_handler(edit_btw_handler)

    # Overview callback
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
