import streamlit as st
import speech_recognition as sr

st.title("🎤 Simple Speech Transcription App")

st.write("Click the button below and start speaking when prompted.")

if st.button(" Start Recording"):

    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening... please speak now.")
        audio = r.listen(source)
        st.success("✅ Done recording!")

    st.write("⏳ Transcribing...")
    try:
        text = r.recognize_google(audio)
        st.success("📝 Transcription:")
        st.write(text)
    except sr.UnknownValueError:
        st.error("😕 Could not understand audio.")
    except sr.RequestError:
        st.error(
            "⚠ Could not request results from Google Speech Recognition service.")
