import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8761347426:AAFQy45nMeaPBQF0uiPuyBlIb1AKNoJzFlA")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# OCR Configuration (Gemini API via OpenAI-compatible endpoint)
# Users can get a free API key from Google AI Studio
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Database Configuration
DB_PATH = "bot_database.db"

# Burmese Messages
MESSAGES = {
    "start": "မင်္ဂလာပါ! KBZPay နှင့် WavePay ပြေစာများကို စစ်ဆေးပေးမည့် Bot ဖြစ်ပါသည်။ ပြေစာပုံကို ပို့ပေးပါ။",
    "help": "ပြေစာပုံကို ပို့ပေးရုံဖြင့် Transaction ID နှင့် အချက်အလက်များကို စစ်ဆေးပေးမည် ဖြစ်ပါသည်။\n\nAdmin Commands:\n/stats - စာရင်းကြည့်ရန်\n/blacklist <ID> - Blacklist သွင်းရန်\n/unblacklist <ID> - Blacklist မှ ဖယ်ရန်",
    "processing": "ခေတ္တစောင့်ဆိုင်းပေးပါ... ပြေစာကို စစ်ဆေးနေပါသည်။",
    "duplicate_alert": "⚠️ သတိပေးချက် - ဤ Transaction ID ({id}) သည် ယခင်က တင်သွင်းပြီးသား ဖြစ်ပါသည်။",
    "blacklist_alert": "🚫 သတိပေးချက် - ဤ ID ({id}) သည် Blacklist ထဲတွင် ရှိနေပါသည်။",
    "success": "✅ ပြေစာ စစ်ဆေးမှု အောင်မြင်ပါသည်။\n\nApp: {app}\nID: {id}\nပမာဏ: {amount}\nနေ့စွဲ: {date}",
    "error_ocr": "❌ ပြေစာကို ဖတ်၍မရပါ။ ကျေးဇူးပြု၍ ပုံကြည်လင်စွာ ပြန်ရိုက်ပေးပါ။",
    "error_general": "❌ အမှားအယွင်းတစ်ခု ဖြစ်ပေါ်သွားပါသည်။ နောက်မှ ပြန်ကြိုးစားကြည့်ပါ။",
    "admin_only": "❌ ဤ Command ကို Admin သာ အသုံးပြုနိုင်ပါသည်။",
    "blacklist_added": "✅ ID {id} ကို Blacklist ထဲသို့ ထည့်သွင်းပြီးပါပြီ။",
    "blacklist_removed": "✅ ID {id} ကို Blacklist မှ ဖယ်ရှားပြီးပါပြီ။",
}
