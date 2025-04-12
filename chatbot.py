import requests
import json
import streamlit as st

# Set your weather context here or dynamically update from external API
WEATHER_CONTEXT = "The weather today is sunny with a high of 75°F (24°C) and a low of 55°F (13°C)."

# --- Function to call OpenRouter API ---
def get_ai_response(prompt, weather_context):
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",  # Or replace with your key directly for testing
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openchat/openchat-7b",  # You can replace with any supported model
            "messages": [
                {
                    "role": "user",
                    "content": f"{weather_context} {prompt}"
                }
            ],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()

        # 🔍 Debug (optional)
        # st.write("API Response:", data)

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "AI response not available. Please try again."

    except requests.exceptions.RequestException as e:
        return f"❌ API request error: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"❌ Error parsing API response: {e}"


# --- Streamlit UI Function ---
def display_chat_ui():
    st.title("☀️ Weather AI Chatbot")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Default prompts
    default_prompts = [
        "Can I go out today?",
        "What should I wear today?",
        "Is it a good day for outdoor activities?",
        "Will it rain today?",
        "What is the current temperature?",
    ]

    # Layout with prompt buttons
    cols = st.columns(len(default_prompts))
    for i, default_prompt in enumerate(default_prompts):
        if cols[i].button(default_prompt):
            st.session_state.selected_prompt = default_prompt

    # User input or button click
    prompt = st.chat_input("Ask about the weather...")
    if 'selected_prompt' in st.session_state:
        prompt = st.session_state.pop('selected_prompt')

    if prompt:
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI reply
        ai_reply = get_ai_response(prompt, WEATHER_CONTEXT)

        # Display AI reply
        st.chat_message("assistant").markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})


# --- Run the chatbot UI ---
display_chat_ui()
