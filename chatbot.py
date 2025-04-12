import requests
import json
import streamlit as st
import time

def get_ai_response(prompt, weather_context, max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
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
                    print(f"Attempt {attempt + 1}: Unexpected content format: {content}") #added print
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return "AI response format unexpected after retries."
            else:
                print(f"Attempt {attempt + 1}: Unexpected response structure: {response_json}") #added print
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return "AI response structure incomplete after retries."

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: API request error: {e}") #added print
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"API request failed after retries: {e}"
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Attempt {attempt + 1}: JSON parsing error: {e}") #added print
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"JSON parsing failed after retries: {e}"
    return "Unknown error occurred."

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
