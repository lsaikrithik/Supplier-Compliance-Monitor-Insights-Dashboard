# utils.py
import requests
import os

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
    print(f"Payload sent to Gemini API: {payload}")  # Logging
    response = requests.post(url, headers=headers, json=payload)
    
    # Error Handling
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Failed to get response from Gemini API")
    
    result = response.json()
    print(f"Response from Gemini API: {result}")  # Logging

    # Correctly extract the generated text from the response
    if 'candidates' in result and len(result['candidates']) > 0:
        candidate = result['candidates'][0]
        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
            generated_text = candidate['content']['parts'][0]['text']
            print(f"Generated Text: {generated_text}")  # Logging
            return generated_text.strip()
    print("Error: No valid response from Gemini API")
    return "No insights available."

def generate_insights(supplier, records):
    compliance_issues = [f"{r.metric}: {r.status} on {r.date_recorded}" for r in records]
    data_to_analyze = "\n".join(compliance_issues)

    prompt = f"""
    Supplier: {supplier.name}
    Contract Terms: {supplier.contract_terms}
    Compliance Records:
    {data_to_analyze}

    Based on the compliance history, provide specific recommendations for improving compliance and adjusting contract terms.
    """
    print(f"Prompt for generate_insights: {prompt}")  # Logging

    response = gemini_api_request(prompt)
    insights = response.strip()
    return insights
