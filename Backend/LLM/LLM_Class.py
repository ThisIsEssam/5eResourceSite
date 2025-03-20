# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-7942452fffc34173a7b3630a6e3103aa", base_url="https://api.deepseek.com")

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




