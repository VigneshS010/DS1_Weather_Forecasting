import requests

GOOGLE_GEMINI_API_KEY = "AIzaSyARPAW72dGnvco9YILGZjcZP9AGakxtv3I"  # Replace with your actual Gemini API key

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [
        {
            "parts": [{"text": "Explain how AI works"}]
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    response_json = response.json()

    if "candidates" in response_json and response_json["candidates"]:
        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        print(generated_text)
    else:
        print("Gemini API response structure incomplete.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except (KeyError, IndexError) as e:
    print(f"An error occurred during parsing: {e}")
