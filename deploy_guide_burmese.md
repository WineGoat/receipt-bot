# Telegram Bot အသုံးပြုနည်းနှင့် Deployment လမ်းညွှန် (ဖုန်းဖြင့် လုပ်ဆောင်ရန်)

ဤလမ်းညွှန်ချက်သည် KBZPay/WavePay Receipt Checker Bot ကို Railway သို့မဟုတ် Render တွင် အခမဲ့ Host လုပ်နည်းကို အသေးစိတ် ရှင်းပြထားပါသည်။

## အဆင့် (၁) လိုအပ်သော Key များ ရယူခြင်း

၁။ **Telegram Bot Token**: 
   - Telegram တွင် [@BotFather](https://t.me/BotFather) ကို ရှာပါ။
   - `/newbot` ဟု ရိုက်ပြီး Bot အသစ်ဆောက်ပါ။
   - ရလာသော **API Token** ကို သိမ်းထားပါ။

၂။ **Gemini API Key** (OCR အတွက်):
   - [Google AI Studio](https://aistudio.google.com/) သို့ သွားပါ။
   - "Get API key" ကို နှိပ်ပြီး Key အသစ်တစ်ခု ယူပါ။ ၎င်းသည် ပြေစာများကို ဖတ်ရန်အတွက် အခမဲ့ အသုံးပြုနိုင်ပါသည်။

၃။ **Admin ID**:
   - Telegram တွင် [@userinfobot](https://t.me/userinfobot) ကို ရှာပြီး သင့်ရဲ့ **User ID** (ဂဏန်းများ) ကို ယူထားပါ။

---

## အဆင့် (၂) GitHub တွင် Code တင်ခြင်း

ဖုန်းဖြင့် လုပ်ဆောင်မည်ဆိုပါက GitHub App သို့မဟုတ် Browser ကို အသုံးပြုနိုင်ပါသည်။

၁။ [GitHub.com](https://github.com) တွင် Account ဖွင့်ပါ။
၂။ Repository အသစ်တစ်ခု ဆောက်ပါ (ဥပမာ- `myanmar-receipt-bot`)။
၃။ ကျွန်ုပ်ပေးထားသော File အားလုံးကို ထို Repository ထဲသို့ Upload တင်ပါ။

---

## အဆင့် (၃) Railway တွင် Deploy လုပ်နည်း (အကြံပြုချက်)

Railway သည် ဖုန်းဖြင့် အသုံးပြုရ လွယ်ကူပြီး အခမဲ့ အသုံးပြုနိုင်သော ပမာဏ ပေးထားပါသည်။

၁။ [Railway.app](https://railway.app/) သို့ သွားပြီး GitHub ဖြင့် Login ဝင်ပါ။
၂။ **"New Project"** ကို နှိပ်ပါ။
၃။ **"Deploy from GitHub repo"** ကို ရွေးပြီး သင့် Repository ကို ရွေးပါ။
၄။ **"Variables"** Tab သို့ သွားပြီး အောက်ပါတို့ကို ထည့်ပါ-
   - `TELEGRAM_TOKEN`: (သင့် Bot Token)
   - `GEMINI_API_KEY`: (သင့် Gemini Key)
   - `ADMIN_IDS`: (သင့် User ID)
၅။ **"Deploy"** ကို နှိပ်ပါ။ ခေတ္တစောင့်လျှင် Bot စတင် အလုပ်လုပ်ပါလိမ့်မည်။

---

## အဆင့် (၄) Bot ကို အသုံးပြုခြင်း

၁။ သင့် Bot ထဲသို့ သွားပြီး `/start` ကို နှိပ်ပါ။
၂။ ပြေစာပုံ တစ်ပုံ ပို့ကြည့်ပါ။
၃။ Bot က Transaction ID ကို ဖတ်ပြီး Duplicate ဖြစ်မဖြစ် စစ်ဆေးပေးပါလိမ့်မည်။

### Admin Commands:
- `/stats`: Bot ၏ အခြေအနေကို ကြည့်ရန်။
- `/blacklist <ID>`: လူလိမ် ID များကို ပိတ်ထားရန်။
- `/unblacklist <ID>`: Blacklist မှ ပြန်ဖြုတ်ရန်။

---

## အရေးကြီးသော မှတ်ချက်များ
- ဤ Bot သည် SQLite Database ကို အသုံးပြုထားပါသည်။ Railway တွင် အမြဲတမ်း သိမ်းဆည်းထားနိုင်ရန် "Volume" ထည့်သွင်းရန် လိုအပ်နိုင်ပါသည်။ (သို့မဟုတ်) အခမဲ့ အဆင့်တွင် Database သည် Restart ချတိုင်း ပျက်သွားနိုင်ပါသည်။
- ပြေစာပုံများသည် ကြည်လင်ပြတ်သားရန် လိုအပ်ပါသည်။

သင့်အတွက် အဆင်ပြေမည်ဟု မျှော်လင့်ပါသည်။ မရှင်းလင်းသည်များ ရှိပါက မေးမြန်းနိုင်ပါသည်။
