# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=open_ai_key, base_url="https://api.deepseek.com")

def get_llm_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Hello"}
        ],
        max_tokens=200,
        stream=False
    )
    return response.choices[0].message.content




