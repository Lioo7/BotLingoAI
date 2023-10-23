from gtts import gTTS
import sys
sys.path.append("../")
from logs.logging import logger

def convert_text_to_audio(text: str) -> None:
    try:
        # Create a gTTS object
        tts = gTTS(text)

        # Save the audio to a file
        output_file = "output.mp3"
        tts.save(output_file)

        logger.info("Audio saved as %s", output_file)
    except Exception as e:
        logger.error("An error occurred while converting text to audio: %s", str(e))

# if __name__ == "__main__":
#     text_to_convert = "Hey, my name is Lior Atyia, and I am your English tutor"
#     convert_text_to_audio(text_to_convert)