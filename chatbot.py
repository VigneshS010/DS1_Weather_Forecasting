import requests
import json
import streamlit as st

# Fetch the API key securely from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]  # Replace with your actual key in secrets.toml

def get_ai_response(prompt, weather_context):
    try:
        # Prepare the request payload
        data_payload = {
            "model": "google/gemini-2.0-flash-exp:free",  # Make sure to use the correct model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{weather_context} {prompt}"  # Add the weather context to the prompt
                        }
                    ]
                }
            ]
        }

        # Make the POST request to the API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional, can be left blank or replaced with your site URL
                "X-Title": "<YOUR_SITE_NAME>",  # Optional, can be left blank or replaced with your site title
            },
            data=json.dumps(data_payload)
        )

        response.raise_for_status()  # Raise an error for bad status codes (e.g., 400 or 500)
        
        # Parse the JSON response
        response_json = response.json()

        # Check if the response contains valid data
        if "choices" in response_json and len(response_json["choices"]) > 0:
            content = response_json["choices"][0].get("message", {}).get("content", None)

            if content:
                # Return the AI-generated response
                return content if isinstance(content, str) else content[0].get("text", "Unknown response format")
            else:
                return "AI response format unexpected."

        else:
            return "AI response structure incomplete."

    except requests.exceptions.RequestException as e:
        return f"An error occurred during the API request: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"An error occurred while parsing the API response: {e}"

def display_chat_ui():
    st.subheader("Chat with AI")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about the weather...")

    # Default prompts for the user
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
