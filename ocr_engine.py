import base64
import json
from openai import OpenAI
from config import GEMINI_API_KEY

def process_receipt_image(image_path):
    """
    Processes the receipt image using Gemini API.
    Returns a dictionary with extracted data or None if failed.
    """
    if not GEMINI_API_KEY:
        return {"error": "Gemini API Key not configured"}

    try:
        client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        prompt = """You are a Myanmar mobile payment receipt analyzer. 
Analyze this image carefully. It should be a KBZPay or WavePay payment receipt/screenshot from Myanmar.

If this is NOT a payment receipt (e.g., it's a random image, meme, or unrelated photo), respond with:
{"error": "not_receipt"}

If this IS a payment receipt, extract the following information and respond in JSON format:
{
    "app": "KBZPay" or "WavePay" (determine from the receipt design/logo),
    "transaction_id": "the transaction number/ID shown on receipt",
    "amount": "the payment amount with Ks (e.g., 36,000 Ks)",
    "date": "transaction date and time",
    "sender": "sender name if visible",
    "receiver": "receiver name if visible",
    "is_fake": true or false,
    "fake_reason": "reason if fake, empty string if not fake"
}

To detect FAKE receipts, check for:
- Inconsistent fonts or text alignment
- Unusual spacing between elements
- Blurry or pixelated text while other parts are clear
- Wrong format for KBZPay/WavePay receipts
- Transaction ID format doesn't match standard patterns
- KBZPay transaction IDs are typically 16-20 digits
- WavePay transaction IDs typically start with specific prefixes

Respond ONLY with the JSON object, nothing else."""

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )

        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        if response_text.startswith("```"):
            # Remove markdown code blocks
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(response_text)
        return result

    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}, Response: {response_text}")
        return None
    except Exception as e:
        print(f"OCR Error: {e}")
        return None
