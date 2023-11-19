import os

import openai
from dotenv import load_dotenv

from logs.logging import logger

load_dotenv()

# Check for required environment variables
if (
    "OPENAI_ORGANIZATION" not in os.environ
    or "OPENAI_API_KEY" not in os.environ
):
    raise ValueError(
        "Missing OpenAI environment variables. Please set OPENAI_ORGANIZATION\
            and OPENAI_API_KEY."
    )

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants for system messages
TEXT_SYSTEM_MESSAGE = (
    "I want you to act as a spoken English teacher and improver. "
    "I will speak to you in English, and you will reply to me in English "
    "to practice my spoken English. I want you to keep your reply neat, "
    "limiting the response to 100 words. I want you to strictly correct "
    "my grammar mistakes, typos, and factual errors. I want you to ask "
    "me a question in your reply."
)
VOICE_SYSTEM_MESSAGE = (
    "I want you to act as a spoken English teacher and improver. "
    "I'll transcribe your message and ask for corrections in "
    "speaking-related issues, excluding pronunciation. Please "
    "focus on improving fluency, expression, and other spoken "
    "aspects. Keep your response under 100 words and include a "
    "question for interactive practice."
)


def validate_user_input(
    user_input: str,
):
    """
    Validates the length and content of user input.

    Args:
    - user_input (str): The user's input.

    Returns:
    - bool: True if the user input is non-empty and within the maximum length,\
          False otherwise.
    """
    MAX_USER_INPUT_LENGTH = 500
    if not user_input.strip():
        logger.warning("Empty user input received.")
        return False

    if len(user_input.strip()) > MAX_USER_INPUT_LENGTH:
        logger.warning(
            f"User input exceeds maximum length {MAX_USER_INPUT_LENGTH}"
        )
        return False

    return True


def process_interaction(
    user_input: str,
    system_message: str,
    model="gpt-3.5-turbo",
):
    """
    Handles the interaction between the user and the ChatGPT model.

    Args:
    - user_input (str): The user's input.
    - system_message (str): The system message guiding the conversation.
    - model (str): The OpenAI model to use (default is "gpt-3.5-turbo").

    Returns:
    - str: The response generated by the ChatGPT model.
    """
    try:
        if not validate_user_input(user_input):
            return "Please provide a non-empty user input."

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )
        response_content = (
            response["choices"][0]
            .get(
                "message",
                {},
            )
            .get(
                "content",
                "",
            )
        )
        return response_content

    except openai.error.OpenAIError as e:
        logger.error(f"An OpenAI error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def process_text_interaction(
    user_input,
    model="gpt-3.5-turbo",
):
    """
    Handles the interaction when users communicate through text messages.

    Args:
    - user_input (str): The user's input.
    - model (str): The OpenAI model to use (default is "gpt-3.5-turbo").

    Returns:
    - str: The response generated by the ChatGPT model.
    """
    return process_interaction(
        user_input,
        TEXT_SYSTEM_MESSAGE,
        model,
    )


def process_voice_interaction(
    user_input,
    model="gpt-3.5-turbo",
):
    """
    Manages the interaction when users communicate through voice messages,
    including transcription and spoken-related corrections.

    Args:
    - user_input (str): The user's input.
    - model (str): The OpenAI model to use (default is "gpt-3.5-turbo").

    Returns:
    - str: The response generated by the ChatGPT model.
    """
    return process_interaction(
        user_input,
        VOICE_SYSTEM_MESSAGE,
        model,
    )
