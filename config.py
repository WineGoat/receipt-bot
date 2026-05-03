import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", os.getenv("TELEGRAM_TOKEN", ""))
ADMIN_IDS = []

# Support both ADMIN_ID (single) and ADMIN_IDS (multiple)
admin_id_single = os.getenv("ADMIN_ID", "")
admin_ids_multi = os.getenv("ADMIN_IDS", "")

if admin_id_single:
    ADMIN_IDS.append(int(admin_id_single))
if admin_ids_multi:
    ADMIN_IDS.extend([int(id.strip()) for id in admin_ids_multi.split(",") if id.strip()])

# OCR Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database Configuration
DB_PATH = "bot_database.db"

# Burmese Messages
MESSAGES = {
    "start": "မင်္ဂလာပါ! KBZPay နှင့် WavePay ပြေစာများကို စစ်ဆေးပေးမည့် Bot ဖြစ်ပါသည်။\n\nပြေစာ screenshot ကို ပို့ပေးပါ။\n\nAdmin Commands:\n/stats - စာရင်းကြည့်ရန်\n/blacklist <ID> - Blacklist သွင်းရန်\n/unblacklist <ID> - Blacklist မှ ဖယ်ရန်",
    "help": "ပြေစာ screenshot ကို ပို့ပေးရုံဖြင့် Transaction ID နှင့် အချက်အလက်များကို စစ်ဆေးပေးမည် ဖြစ်ပါသည်။\n\nAdmin Commands:\n/stats - စာရင်းကြည့်ရန်\n/blacklist <ID> - Blacklist သွင်းရန်\n/unblacklist <ID> - Blacklist မှ ဖယ်ရန်",
    "processing": "⏳ ခေတ္တစောင့်ဆိုင်းပေးပါ... ပြေစာကို စစ်ဆေးနေပါသည်။",
    "duplicate_alert": "⚠️ သတိပေးချက် - ဤ Transaction ID ({id}) သည် ယခင်က တင်သွင်းပြီးသား ဖြစ်ပါသည်။ နှစ်ခါပြန်ပို့ထားခြင်း ဖြစ်နိုင်ပါသည်။",
    "blacklist_alert": "🚫 သတိပေးချက် - ဤ ID ({id}) သည် Blacklist ထဲတွင် ရှိနေပါသည်။ ဤပြေစာကို လက်မခံပါနှင့်။",
    "success": "✅ ပြေစာ စစ်ဆေးမှု ပြီးပါပြီ။\n\n📱 App: {app}\n🔢 Transaction ID: {id}\n💰 ပမာဏ: {amount}\n📅 နေ့စွဲ: {date}",
    "error_ocr": "❌ ပြေစာကို ဖတ်၍မရပါ။ ကျေးဇူးပြု၍ ပြေစာ screenshot ကို ပိုရှင်းအောင် ပြန်ရိုက်ပြီး ပို့ပေးပါ။",
    "error_general": "❌ အမှားအယွင်းတစ်ခု ဖြစ်ပေါ်သွားပါသည်။ နောက်မှ ပြန်ကြိုးစားကြည့်ပါ။",
    "admin_only": "❌ ဤ Command ကို Admin သာ အသုံးပြုနိုင်ပါသည်။",
    "blacklist_added": "✅ ID {id} ကို Blacklist ထဲသို့ ထည့်သွင်းပြီးပါပြီ။",
    "blacklist_removed": "✅ ID {id} ကို Blacklist မှ ဖယ်ရှားပြီးပါပြီ။",
}
