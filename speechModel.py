from gtts import gTTS
import pygame
import time
import os

def text_to_speech(response_text):
    """Convert text response to speech and play it."""
    
    # Generate speech from text
    tts = gTTS(text=response_text, lang="en")
    audio_file = "response_audio.mp3"
    
    # Save the generated audio
    tts.save(audio_file)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Remove the audio file after playing
    os.remove(audio_file)

# Example usage (Remove this when integrating with LLaMA)
if __name__ == "__main__":
    sample_text = "Hello! This is a test response from LLaMA."
    text_to_speech(sample_text)
