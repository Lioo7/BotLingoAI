# import sys

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

# sys.path.append("../")
# from os import path

from logs.logging import logger


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


def convert_text_to_audio(text: str, output_name: str) -> None:
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


def convert_audio_to_text(audio_file: str) -> str:
    try:
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            # Adjust for ambient noise and record audio
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)

        # Recognize the speech in the audio
        text = recognizer.recognize_google(audio, language="en")
        return text
    except sr.UnknownValueError:
        logger.warning(
            "Google Speech Recognition could not understand the audio."
        )
        return ""
    except sr.RequestError as e:
        logger.error(
            "Could not request results from Google Speech Recognition service: %s",
            str(e),
        )
        return ""


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


# if __name__ == "__main__":
#     text_to_convert = "Hey, my name is Lior Atiya and I'm your English tutor"
#     mp3_output_name = "output.mp3"
#     wav_output_file = "output.wav"

#     # Convert text to audio
#     convert_text_to_audio(text_to_convert, mp3_output_name)

#     # # Convert MP3 to WAV
#     # convert_mp3_to_wav(mp3_output_file, wav_output_file)

#     # # Extract text from the WAV file
#     # result = convert_audio_to_text(wav_output_file)

#     # if result:
#     #     print("Converted Text:")
#     #     print(result)
