from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize(input_text, action):
    
    if action == "tldr":
        from modules.prompts import tldr_prompt # System prompt
        system = tldr_prompt
        text = input_text
    elif action == "merge":
        from modules.prompts import merge_prompt # System prompt
        system = merge_prompt
        text = "\n".join(input_text)
        text = "Summaries:\n" + text

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model = "gpt-4",
        messages=messages,
        temperature=0.5,
    )
    chat_completion = response.choices[0].message.content
    tokens_used = response.usage.total_tokens

    # Debug: Print Total Tokens
    print(tokens_used)
    return chat_completion
