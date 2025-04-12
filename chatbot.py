# chatbot.py
import requests
import json

OPENROUTER_API_KEY = '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'

def get_ai_response(prompt, weather_context):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
                        ],
                    },
                ],
            }),
        )
        response.raise_for_status()
        response_json = response.json()

        if "choices" in response_json and len(response_json["choices"]) > 0 and \
                "message" in response_json["choices"][0] and "content" in response_json["choices"][0]["message"]:

            content = response_json["choices"][0]["message"]["content"]

            if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict) and "text" in content[0]:
                return content[0]["text"]
            elif isinstance(content, str):
                return content
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
