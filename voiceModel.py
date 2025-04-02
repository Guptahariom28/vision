import os
import groq
import speech_recognition as sr
from pydub import AudioSegment

# Set up Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("Recording... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
            print("Recording complete!")
        except sr.WaitTimeoutError:
            print("No speech detected. Recording stopped.")
            return None

    # Save as WAV first
    audio_path_wav = "user_audio.wav"
    with open(audio_path_wav, "wb") as f:
        f.write(audio.get_wav_data())
    
    # Convert WAV to MP3
    audio_path_mp3 = "user_audio.mp3"
    AudioSegment.from_wav(audio_path_wav).export(audio_path_mp3, format="mp3")
    os.remove(audio_path_wav)  # Remove temp WAV file
    return audio_path_mp3

def transcribe_audio(audio_file):
    print("Transcribing audio...")
    response = client.chat.completions.create(
        model="whisper-large-v3",
        messages=[
            {"role": "system", "content": "Transcribe the given audio file accurately."},
            {"role": "user", "content": f"[file: {audio_file}]"}
        ]
    )
    transcription = response.choices[0].message.content
    print("Transcription:", transcription)
    return transcription

if __name__ == "__main__":
    audio_file = record_audio()
    if audio_file:
        transcribe_audio(audio_file)
