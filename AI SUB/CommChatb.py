import torch
import streamlit as st
import pandas as pd
from transformers import pipeline
import speech_recognition as sr
import difflib

# Load your dataset
df = pd.read_excel(
    "C:/Users/DZMap/Desktop/AI/communication_chatbot_dataset (1).xlsx").fillna("")
context = df.astype(str).agg('. '.join, axis=1)
context_text = "\n".join(context)

# Load the model pipeline
generator = pipeline("text2text-generation", model="google/flan-t5-base")


def get_improvement(user_input):
    prompt = (
        "Use the following data to answer the question. If not available, say 'No information found.'\n\n"
        f"Data:\n{context_text}\n\nQuestion: {user_input}\nAnswer:"
    )
    answer = generator(prompt, max_new_tokens=150, do_sample=False)[
        0]['generated_text']
    return answer.strip()


def highlight_differences(original, improved):
    # Generate a diff of the original vs improved sentence
    diff = list(difflib.ndiff(original.split(), improved.split()))
    highlighted_text = ""
    for token in diff:
        word = token[2:]
        if token.startswith("-"):
            # Removed words shown in red
            highlighted_text += f'<span style="background-color:#ffb3b3;text-decoration:line-through;">{word} </span>'
        elif token.startswith("+"):
            # Added words shown in green
            highlighted_text += f'<span style="background-color:#b3ffb3;">{word} </span>'
        else:
            # Unchanged words normal
            highlighted_text += f"{word} "
    return highlighted_text


st.set_page_config(
    page_title="Communication Improvement Chatbot", layout="centered")

st.markdown("<h1 style='text-align: center; color: navy;'>Communication Improvement Chatbot</h1>",
            unsafe_allow_html=True)
st.markdown("---")

user_option = st.radio("Select your input method:", ("Type", "Speak"))


if user_option == "Type":
    user_text = st.text_input("Enter your message:")
    if user_text:
        improved = get_improvement(user_text)
        st.markdown("### Improved way to say:")
        # Show original and improved side by side with highlights
        highlighted = highlight_differences(user_text, improved)
        st.markdown(f"<b>Original:</b> {user_text}")
        st.markdown(
            f"<b>Improved:</b> <span>{highlighted}</span>", unsafe_allow_html=True)

elif user_option == "Speak":
    st.write("Click below and speak your message.")
    if st.button("Start Recording"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎧 Listening... please speak now.")
            # audio = r.listen(source)
            audio = r.listen(source, phrase_time_limit=8)
            st.success("✅ Done recording!")
        st.write("⏳ Transcribing...")
        try:
            transcribed_text = r.recognize_google(audio)
            st.markdown("### Transcribed:")
            st.info(transcribed_text)
            improved = get_improvement(transcribed_text)
            st.markdown("### Improved way to say:")
            highlighted = highlight_differences(transcribed_text, improved)
            st.markdown(f"<b>Original:</b> {transcribed_text}")
            st.markdown(
                f"<b>Improved:</b> <span>{highlighted}</span>", unsafe_allow_html=True)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Request error from the speech service.")
