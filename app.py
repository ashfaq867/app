import streamlit as st
import soundfile as sf
import pyaudio
import wave
from transformers import pipeline
import os

# Function to record audio
def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    st.warning("Recording... Click 'Stop Recording' when done.")
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.warning("Recording... Click 'Stop Recording' when done.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

# Function for transcribing audio using Hugging Face's pipeline
p = pipeline("automatic-speech-recognition")

def transcribe(audio_file):
    audio_text = p(audio_file)[0]["text"]
    return audio_text

# Streamlit App
def main():
    st.title("Speech-to-Text App")

    # Audio Recorder
    st.subheader("Record Audio")
    recording_state = st.text_area("Recording State:", value="", height=100)
    if st.button("Start Recording"):
        recording_state = ""
        recording_state += "Recording started. "
        record_audio("temp_audio.wav")  # Record audio to a temporary file
    if st.button("Stop Recording"):
        recording_state += "Recording stopped. "

    # Transcribe Recorded Audio
    st.subheader("Transcribe Recorded Audio")
    if st.button("Transcribe"):
        if "Recording stopped." in recording_state:
            audio_text = transcribe("temp_audio.wav")
            st.text_area("Transcription Result:", value=audio_text, height=200)
        else:
            st.error("Please stop recording before transcribing.")

    # Delete the temporary audio file
    if "Recording stopped." in recording_state:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

if __name__ == "__main__":
    main()
