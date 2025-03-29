import openai

def extract_receipt_data(raw_text: str) -> dict:
    prompt = f"""Extract structured receipt data from this text:
{raw_text}

Return this format:
{{"vendor": "", "date": "", "total": "", "items": [{{"name": "", "qty": "", "price": ""}}]}}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return eval(response.choices[0].message.content)
