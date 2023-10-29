import speech_recognition as sr
from os import path
from pydub import AudioSegment

def transcribe_voice_message(file_id):
    # Load the OGG file
    ogg_audio = AudioSegment.from_file(f"bot/voice_messages/{file_id}.ogg", format="ogg")

    # Export it as WAV
    ogg_audio.export(f"bot/voice_messages/{file_id}.wav", format="wav")

    # transcribe audio file
    AUDIO_FILE = f"bot/voice_messages/{file_id}.wav"

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

        print("Transcription: " + r.recognize_google(audio))
