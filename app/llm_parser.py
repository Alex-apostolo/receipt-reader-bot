import openai
import base64
from typing import Union
from app.config import OPENAI_API_KEY

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def extract_receipt_data(image_data: Union[str, bytes, bytearray]) -> dict:
    # If the input is a file path (string), read it
    if isinstance(image_data, str):
        with open(image_data, "rb") as file:
            image_data = file.read()

    # Convert image data to base64
    if isinstance(image_data, (bytes, bytearray)):
        image_data = base64.b64encode(image_data).decode("utf-8")

    prompt = f"""Extract structured receipt data from this image:
{image_data}

Return this format:
{{"vendor": "", "date": "", "total": "", "items": [{{"name": "", "qty": "", "price": ""}}]}}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content
