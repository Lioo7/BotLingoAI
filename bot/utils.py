import os

import boto3
import speech_recognition as sr
from typing import List, Union
from dotenv import load_dotenv
from gtts import gTTS
from pydub import AudioSegment

from logs.logging import logger


load_dotenv()

# Check for required environment variables
if (
    "AWS_ACCESS_KEY_ID" not in os.environ
    or "AWS_SECRET_ACCESS_KEY" not in os.environ
):
    raise ValueError(
        "Missing AWS environment variables. Please set AWS_ACCESS_KEY_ID\
            and AWS_SECRET_ACCESS_KEY."
    )

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "us-east-1"


def transcribe_voice_message(file_id: str) -> str:
    try:
        # Load the OGG file
        ogg_audio = AudioSegment.from_file(
            f"bot/voice_messages/{file_id}.ogg", format="ogg"
        )

        # Export it as WAV
        ogg_audio.export(f"bot/voice_messages/{file_id}.wav", format="wav")

        # Transcribe audio file
        AUDIO_FILE = f"bot/voice_messages/{file_id}.wav"

        # Use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # Read the entire audio file

        transcription = r.recognize_google(audio)
        logger.info(f"Transcription for file {file_id}: {transcription}")
        print(f"Bot: Transcription for file {file_id}: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Error transcribing file {file_id}: {str(e)}")
        print(f"Error transcribing file {file_id}: {str(e)}")
        raise


def convert_text_to_audio(text: str, output_name: str, provider: str = "aws"):
    try:
        if provider == "google":
            convert_text_to_audio_google(text, output_name)
        elif provider == "aws":
            convert_text_to_audio_aws(text, output_name)
        else:
            raise Exception("Invalid provider specified")
    except Exception as e:
        logger.error(f"Error in convert_text_to_audio: {str(e)}")


def convert_text_to_audio_google(text: str, output_name: str) -> None:
    try:
        # Specify the language code
        language = "en"

        # Create a gTTS object with the specified language
        tts = gTTS(text, lang=language)

        # Save the audio to the specified file
        tts.save(f"bot/voice_messages/{output_name}")

        logger.info("Audio saved as %s", output_name)
    except Exception as e:
        logger.error(
            "An error occurred while converting text to audio: %s", str(e)
        )


def convert_text_to_audio_aws(text: str, output_name: str) -> None:
    try:
        # Create a Polly client
        polly = boto3.client(
            "polly",
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Specify the voice you want to use
        # https://docs.aws.amazon.com/polly/latest/dg/ntts-voices-main.html
        voice_id = "Ruth"

        # Synthesize speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,
            Engine="neural",  # Specify the engine as 'neural' for NTTS
        )

        # Save the audio stream to a file
        with open(f"bot/voice_messages/{output_name}", "wb") as file:
            file.write(response["AudioStream"].read())

        logger.info("Audio saved as %s", output_name)
    except Exception as e:
        logger.error(
            "An error occurred while converting text to audio: %s", str(e)
        )


def convert_mp3_to_wav(mp3_file: str, wav_file: str) -> None:
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file)

        # Export as WAV
        audio.export(wav_file, format="wav")
        logger.info("MP3 file converted to WAV: %s", wav_file)
    except Exception as e:
        logger.error(
            "An error occurred while converting MP3 to WAV: %s", str(e)
        )


def split_review_and_followup(input_string: str) -> List[Union[str, None]]:
    start_index = input_string.find('*')
    end_index = input_string.rfind('*')

    if start_index != -1 and end_index != -1 and start_index < end_index:
        review_text = input_string[:start_index].strip()
        followup_question = input_string[start_index + 1:end_index].strip()

        return [review_text, followup_question]
    else:
        # Return the entire string if no asterisks or they are not properly placed.
        return [input_string, None]
