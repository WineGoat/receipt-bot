import base64
import json
from openai import OpenAI
from config import GEMINI_API_KEY

def process_receipt_image(image_path):
    """
    Processes the receipt image using Gemini 2.5 Flash API.
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

        prompt = """
        Analyze this Myanmar mobile payment receipt (KBZPay or WavePay).
        Extract the following information in JSON format:
        - app: "KBZPay" or "WavePay"
        - transaction_id: The unique transaction ID number
        - amount: The payment amount with currency (e.g., "10,000 Ks")
        - date: The transaction date and time
        - is_fake: Boolean, true if you detect common fake patterns (inconsistent fonts, edited areas)
        - fake_reason: String, reason if is_fake is true

        Respond ONLY with the JSON object.
        """

        response = client.chat.completions.create(
            model="gemini-2.0-flash", # Using the latest flash model
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
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"OCR Error: {e}")
        return None
