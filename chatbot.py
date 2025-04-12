import requests
import json
import streamlit as st

def get_ai_response(prompt, weather_context):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-thinking-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{weather_context} {prompt}"
                            },
                        ]
                    }
                ],
            })
        )
        response.raise_for_status()
        response_json = response.json()

        # Debug log (optional)
        # st.write("API Raw Response:", response_json)

        if "choices" in response_json and len(response_json["choices"]) > 0:
            message = response_json["choices"][0]["message"]
            content = message.get("content")

            if isinstance(content, list) and len(content) > 0:
                text = content[0].get("text", "")
                return text
            elif isinstance(content, str):
                return content
            else:
                return "AI response format unexpected."
        else:
            return "AI response structure incomplete."

    except requests.exceptions.RequestException as e:
        return f"API request error: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"API response parsing error: {e}"

def display_chat_ui():
    st.subheader("🌤️ Chat with the AI Weather Assistant")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display old messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Default weather context (can be updated based on your app)
    weather_context = "Today's forecast is sunny with a high of 30°C and a low of 20°C."

    # Get user input
    prompt = st.chat_input("Ask about the weather...")

    # Default buttons
    default_prompts = [
        "Can I go out today?",
        "What should I wear today?",
        "Is it a good day for outdoor activities?",
        "Will it rain today?",
        "What is the current temperature?",
    ]

    # Handle default button click
    for default_prompt in default_prompts:
        if st.button(default_prompt):
            prompt = default_prompt

    # If user enters prompt (via input or button)
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI reply
        ai_reply = get_ai_response(prompt, weather_context)

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

# Call the UI function in Streamlit app
display_chat_ui()
