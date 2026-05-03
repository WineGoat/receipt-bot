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
    
    # Create temp directory if not exists
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{photo_file.file_id}.jpg"
    await photo_file.download_to_drive(file_path)
    
    status_msg = await update.message.reply_text(MESSAGES["processing"])
    
    # Process with OCR
    data = process_receipt_image(file_path)
    
    # Clean up temp file
    if os.path.exists(file_path):
        os.remove(file_path)
        
    if not data or "error" in data:
        await status_msg.edit_text(MESSAGES["error_ocr"])
        return

    tx_id = str(data.get("transaction_id", ""))
    app = data.get("app", "Unknown")
    amount = data.get("amount", "Unknown")
    date = data.get("date", "Unknown")
    is_fake = data.get("is_fake", False)
    fake_reason = data.get("fake_reason", "")

    if not tx_id:
        await status_msg.edit_text(MESSAGES["error_ocr"])
        return

    # Check Blacklist
    if is_blacklisted(tx_id):
        await update.message.reply_text(MESSAGES["blacklist_alert"].format(id=tx_id))
    
    # Check Duplicate
    if is_duplicate(tx_id):
        await update.message.reply_text(MESSAGES["duplicate_alert"].format(id=tx_id))
    else:
        add_receipt(tx_id, user_id, amount, date)

    # Fake Detection Alert
    response_text = MESSAGES["success"].format(app=app, id=tx_id, amount=amount, date=date)
    if is_fake:
        response_text += f"\n\n⚠️ **သတိပေးချက် - ဤပြေစာသည် အတုဖြစ်နိုင်ခြေရှိပါသည်။**\nအကြောင်းပြချက်: {fake_reason}"
    
    await status_msg.edit_text(response_text, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    s = get_stats()
    text = f"📊 **Bot စာရင်းများ**\n\nစုစုပေါင်းပြေစာ: {s['total_receipts']}\nBlacklist အရေအတွက်: {s['total_blacklist']}"
    await update.message.reply_text(text, parse_mode="Markdown")

async def blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    if not context.args:
        await update.message.reply_text("အသုံးပြုပုံ: /blacklist <ID>")
        return
    
    target_id = context.args[0]
    if add_to_blacklist(target_id, update.effective_user.id):
        await update.message.reply_text(MESSAGES["blacklist_added"].format(id=target_id))
    else:
        await update.message.reply_text("ဤ ID သည် Blacklist ထဲတွင် ရှိနှင့်ပြီးသားပါ။")

async def unblacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(MESSAGES["admin_only"])
        return
    
    if not context.args:
        await update.message.reply_text("အသုံးပြုပုံ: /unblacklist <ID>")
        return
    
    target_id = context.args[0]
    if remove_from_blacklist(target_id):
        await update.message.reply_text(MESSAGES["blacklist_removed"].format(id=target_id))
    else:
        await update.message.reply_text("ဤ ID ကို ရှာမတွေ့ပါ။")

if __name__ == '__main__':
    # Initialize Database
    init_db()
    
    # Build Bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("blacklist", blacklist))
    app.add_handler(CommandHandler("unblacklist", unblacklist))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot is running...")
    app.run_polling()
