import os
import random

import openai
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# List of possible initial questions
initial_questions = [
    "What's your favorite English word?",
    "Tell me about your day in English.",
    "Can you describe your favorite place using English?",
    "Share a fun fact in English.",
]


def greet_user(user_name):
    # Randomly select an initial question
    random_question = random.choice(initial_questions)
    introduction = f"Hello, {user_name}! I am your English Tutor ChatBot. I'm here to help you improve your spoken English. I will correct your mistakes and ask you questions to practice. Let's start with a question: {random_question}"
    return introduction


def respond_to_user(answer, model="gpt-3.5-turbo"):
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


# def main():
#     user_name = input("Please enter your name: ")
#     greeting = greet_user(user_name)
#     print("Teacher:", greeting)

#     while True:
#         user_response = input("You: ")
#         if user_response.lower() == "exit":
#             break
#         response = respond_to_user(user_response)
#         print("Teacher:", response)

# if __name__ == "__main__":
#     main()
