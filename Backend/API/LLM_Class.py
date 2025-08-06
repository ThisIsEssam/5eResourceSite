# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=open_ai_key, base_url="https://api.deepseek.com")

def get_llm_response(prompt, chat_history=None):
    if chat_history is None:
        chat_history = []  # Initialize an empty history if none is provided

    # Add the new user message to the chat history
    chat_history.append({"role": "user", "content": prompt})

    # Send the request with the full chat history
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=chat_history,
        max_tokens=200,
        stream=False
    )

    # Extract the assistant's response
    assistant_response = response.choices[0].message.content

    # Add the assistant's response to the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response, chat_history




