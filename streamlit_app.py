# Import necessary libraries
import streamlit as st
import pyaudio
import wave
import speech_recognition as sr

# Create a function for recording audio
def record_audio(filename, seconds):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Main Streamlit app
def main():
    st.title("Speech-to-Text App")

    # Record button
    if st.button("Record"):
        st.info("Recording started. Click 'Stop' when done.")
        filename = "audio_recording.wav"
        record_audio(filename, seconds=5)
        st.success("Recording saved as audio_recording.wav")

    # Stop button (placeholder, doesn't do anything)
    if st.button("Stop"):
        st.info("Recording stopped.")

    # Transcription button
    if st.button("Transcribe"):
        st.info("Transcribing...")
        recognizer = sr.Recognizer()
        audio_file = "audio_recording.wav"
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio)
            st.write("Transcription:")
            st.write(transcription)
        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
