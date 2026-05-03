import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, ADMIN_IDS, MESSAGES
from database import init_db, add_receipt, is_duplicate, add_to_blacklist, remove_from_blacklist, is_blacklisted, get_stats
from ocr_engine import process_receipt_image

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["start"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["help"])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo_file = await update.message.photo[-1].get_file()
    
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{photo_file.file_id}.jpg"
    await photo_file.download_to_drive(file_path)
    
    status_msg = await update.message.reply_text(MESSAGES["processing"])
    
    data = process_receipt_image(file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    if not data:
        await status_msg.edit_text(MESSAGES["error_ocr"])
        return

    if "error" in data:
        if data["error"] == "not_receipt":
            await status_msg.edit_text("This is not a receipt. Please send a KBZPay or WavePay receipt screenshot.")
        else:
            await status_msg.edit_text(MESSAGES["error_ocr"])
        return

    tx_id = str(data.get("transaction_id", ""))
    app = data.get("app", "Unknown")
    amount = data.get("amount", "Unknown")
    date = data.get("date", "Unknown")
    sender = data.get("sender", "")
    receiver = data.get("receiver", "")
    is_fake = data.get("is_fake", False)
    fake_reason = data.get("fake_reason", "")

    if not tx_id:
        await status_msg.edit_text(MESSAGES["error_ocr"])
        return

    alerts = []

    if is_blacklisted(tx_id):
        alerts.append(MESSAGES["blacklist_alert"].format(id=tx_id))
    
    if is_duplicate(tx_id):
        alerts.append(MESSAGES["duplicate_alert"].format(id=tx_id))
    else:
        add_receipt(tx_id, user_id, amount, date)

    response_text = MESSAGES["success"].format(app=app, id=tx_id, amount=amount, date=date)
    
    if sender:
        response_text += f"\n👤 Sender: {sender}"
    if receiver:
        response_text += f"\n👤 Receiver: {receiver}"

    if is_fake:
        response_text += f"\n\n⚠️ WARNING - This receipt may be FAKE.\nReason: {fake_reason}"
    else:
        response_text += "\n\n✅ Receipt format appears normal."
    
    if alerts:
        response_text += "\n\n" + "\n".join(alerts)

    await status_msg.edit_text(response_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    s = get_stats()
    text = f"📊 Bot Stats\n\nTotal Receipts: {s['total_receipts']}\nBlacklist Count: {s['total_blacklist']}"
    await update.message.reply_text(text)

async def blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /blacklist <Transaction ID>")
        return
    
    target_id = context.args[0]
    if add_to_blacklist(target_id, update.effective_user.id):
        await update.message.reply_text(MESSAGES["blacklist_added"].format(id=target_id))
    else:
        await update.message.reply_text("This ID is already in the Blacklist.")

async def unblacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /unblacklist <Transaction ID>")
        return
    
    target_id = context.args[0]
    if remove_from_blacklist(target_id):
        await update.message.reply_text(MESSAGES["blacklist_removed"].format(id=target_id))
    else:
        await update.message.reply_text("ID not found.")

if __name__ == '__main__':
    init_db()
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("blacklist", blacklist))
    app.add_handler(CommandHandler("unblacklist", unblacklist))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot is running...")
    app.run_polling()
