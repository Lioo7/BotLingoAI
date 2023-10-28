from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import sys
sys.path.append("../")
from logs.logging import logger

def convert_text_to_audio(text: str, output_file: str) -> None:
    try:
        # Specify the language code
        language = "en-US"

        # Create a gTTS object with the specified language
        tts = gTTS(text, lang=language)

        # Save the audio to the specified file
        tts.save(output_file)

        logger.info("Audio saved as %s", output_file)
    except Exception as e:
        logger.error("An error occurred while converting text to audio: %s", str(e))

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
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        logger.warning("Google Speech Recognition could not understand the audio.")
        return ""
    except sr.RequestError as e:
        logger.error("Could not request results from Google Speech Recognition service: %s", str(e))
        return ""

def convert_mp3_to_wav(mp3_file: str, wav_file: str) -> None:
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file)
        
        # Export as WAV
        audio.export(wav_file, format="wav")
        logger.info("MP3 file converted to WAV: %s", wav_file)
    except Exception as e:
        logger.error("An error occurred while converting MP3 to WAV: %s", str(e))

if __name__ == "__main__":
    text_to_convert = "Hey, my name is Lior Atyia, and I am your English tutor"
    mp3_output_file = "output.mp3"
    wav_output_file = "output.wav"

    # Convert text to audio
    convert_text_to_audio(text_to_convert, mp3_output_file)

    # Convert MP3 to WAV
    convert_mp3_to_wav(mp3_output_file, wav_output_file)

    # Extract text from the WAV file
    result = convert_audio_to_text(wav_output_file)

    if result:
        print("Converted Text:")
        print(result)
