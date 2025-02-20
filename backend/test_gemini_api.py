import os , requests
from dotenv import load_dotenv

load_dotenv()

def gemini_api_request(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    if 'candidates' in result and len(result['candidates']) > 0:
        candidate = result['candidates'][0]
        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
            generated_text = candidate['content']['parts'][0]['text']
            return generated_text.strip()
    return "No insights available."

prompt = """
Supplier: Supplier_1
Contract Terms: {'delivery_time': 'within 7 days', 'quality_standard': 'ISO9001', 'discount_rate': 5}
Compliance Records:
Quality: Fail on 2024-09-26
Delivery Time: Non-compliant on 2024-10-07
Delivery Time: Compliant on 2024-10-26
Delivery Time: Non-compliant on 2024-08-26
Delivery Time: Compliant on 2024-10-27
Delivery Time: Compliant on 2024-09-03

Based on the compliance history, provide specific recommendations for improving compliance and adjusting contract terms.
"""
insights = gemini_api_request(prompt)
print("Insights:")
print(insights)
