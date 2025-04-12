import requests
import streamlit as st

GOOGLE_GEMINI_API_KEY = "AIzaSyARPAW72dGnvco9YILGZjcZP9AGakxtv3I"  # Replace with your actual Gemini API key

def get_gemini_response(prompt, weather_context):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{weather_context} {prompt}"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()

        if "candidates" in response_json and response_json["candidates"]:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Gemini API response structure incomplete."

    except requests.exceptions.RequestException as e:
        return f"An error occurred during the API request: {e}"
    except (KeyError, IndexError) as e:
        return f"An error occurred while parsing the API response: {e}"

def display_chat_ui():
    st.subheader("Chat with AI")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about the weather...")

    default_prompts = [
        "Can I go out today?",
        "What should I wear today?",
        "Is it a good day for outdoor activities?",
        "Will it rain today?",
        "What is the current temperature?",
    ]

    for default_prompt in default_prompts:
        if st.button(default_prompt):
            prompt = default_prompt

    return prompt

# Example usage within your main app.py:
# Inside your app.py, where you need the AI response:
# ai_response = get_gemini_response(user_prompt, weather_context)
