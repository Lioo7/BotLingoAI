import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def respond_to_user(answer: str, model: str = "gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "I want you to act as a spoken English teacher and improver. I will speak to you in English, and you will reply to me in English to practice my spoken English. I want you to keep your reply neat, limiting the response to 100 words. I want you to strictly correct my grammar mistakes, typos, and factual errors. I want you to ask me a question in your reply.",
            },
            {"role": "user", "content": answer},
        ],
    )
    response = response["choices"][0]["message"]["content"]
    return response