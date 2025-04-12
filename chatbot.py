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
                    "content": f"{weather_context} {prompt}"  # Add the weather context to the prompt
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

        # Print the full response for debugging
        print("Full Response:", json.dumps(response_json, indent=4))  # This line will print the full response

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

    # Display existing messages in the chat window
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get input from the user (chat input box)
    prompt = st.chat_input("Ask about the weather...")

    # Default prompts for the user
    default_prompts = [
        "Can I go out today?",
        "What should I wear today?",
        "Is it a good day for outdoor activities?",
        "Will it rain today?",
        "What is the current temperature?",
    ]

    # Display default prompt buttons
    for default_prompt in default_prompts:
        if st.button(default_prompt):
            prompt = default_prompt

    # If prompt is not empty
    if prompt:
        # Fetch weather context (this can be an API call to a weather service or hardcoded for demo purposes)
        weather_context = "The current weather in your location is sunny with a temperature of 25°C."  # Example context

        # Get AI response with the weather context
        response = get_ai_response(prompt, weather_context)

        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Add AI response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Scroll to the bottom after new messages
        st.chat_message("assistant").markdown(response)

    return prompt
