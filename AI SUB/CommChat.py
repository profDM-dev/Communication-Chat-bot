# import pandas as pd
# from transformers import pipeline
# df = pd.read_excel("communication_chatbot_dataset (1).xlsx").fillna("")
# context = df.astype(str).agg('. '.join, axis=1)
# context_text = "\n".join(context)

# # ⿣ Load local pretrained model
# generator = pipeline("text2text-generation", model="google/flan-t5-base")

# # ⿤ Ask function


# def ask(query):
#     prompt = f"Use the following data to answer the question. If not available, say 'No information found.'\n\nData:\n{context_text}\n\nQuestion: {query}\nAnswer:"
#     answer = generator(prompt, max_new_tokens=150, do_sample=False)[
#         0]['generated_text']
#     print("\n--- ANSWER ---\n", answer.strip())


# ask("tell me about we was late")

import torch
import streamlit as st
import pandas as pd
from transformers import pipeline
import speech_recognition as sr


df = pd.read_excel(
    "C:/Users/DZMap/Desktop/AI/communication_chatbot_dataset (1).xlsx").fillna("")
context = df.astype(str).agg('. '.join, axis=1)
context_text = "\n".join(context)


generator = pipeline("text2text-generation", model="google/flan-t5-base")


def get_improvement(user_input):
    prompt = (
        "Use the following data to answer the question. If not available, say 'No information found.'\n\n"
        f"Data:\n{context_text}\n\nQuestion: {user_input}\nAnswer:"
    )
    answer = generator(prompt, max_new_tokens=150, do_sample=False)[
        0]['generated_text']
    return answer.strip()


st.title("Communication Improvement Chatbot")

user_option = st.radio("How do you want to provide input?", ("Type", "Speak"))

if user_option == "Type":
    user_text = st.text_input("Enter your message:")
    if user_text:
        improved = get_improvement(user_text)
        st.markdown("**Improved way to say:**")
        st.success(improved)

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
            st.markdown("**Transcribed:**")
            st.info(transcribed_text)
            improved = get_improvement(transcribed_text)
            st.markdown("**Improved way to say:**")
            st.success(improved)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Request error from the speech service.")
