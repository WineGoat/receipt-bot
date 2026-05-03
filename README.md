# Myanmar Receipt Verification Bot (KBZPay & WavePay)

This is a professional Telegram Bot designed for the Myanmar market to verify KBZPay and WavePay receipts. It uses AI-powered OCR to extract transaction details and detect potential frauds.

## Features
- **OCR Verification**: Automatically reads KBZPay and WavePay receipts.
- **Duplicate Detection**: Prevents the same receipt from being used twice.
- **Blacklist System**: Block specific Transaction IDs or Users.
- **Fake Detection**: AI analysis to spot common fake receipt patterns.
- **Admin Panel**: Manage stats and blacklist via Telegram commands.
- **Burmese Language**: All bot responses are in Burmese for local users.

## Setup Instructions

### 1. Get API Keys
- **Telegram Bot Token**: Get it from [@BotFather](https://t.me/BotFather).
- **Gemini API Key**: Get a free API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
TELEGRAM_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
ADMIN_IDS=your_telegram_user_id_here
```

### 3. Installation
```bash
pip install -r requirements.txt
python bot.py
```

## Deployment
For a detailed step-by-step guide on how to deploy this bot for free using only your phone, please refer to `deploy_guide_burmese.md`.

## License
This project is open-source and can be shared or sold by the owner.
