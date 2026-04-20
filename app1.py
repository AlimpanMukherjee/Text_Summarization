import streamlit as st
import os
import tempfile
import shutil

# -------------------- FIX FFMPEG PATH --------------------
os.environ["PATH"] += r";C:\Users\KIIT0001\Desktop\losslesscut\resources"

# -------------------- IMPORTS --------------------
import whisper
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.title(" Video Summarizer")

# -------------------- API KEY --------------------
with st.sidebar:
    groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader(
    "Upload a video file",
    type=["mp4", "mov", "avi", "mkv"]
)

# -------------------- LOAD WHISPER (CACHED) --------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")  # change to 'small' if needed

# -------------------- CHUNK FUNCTION --------------------
def chunk_text(text, size=2000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)

# -------------------- MAIN --------------------
if st.button("Summarize"):

    if not groq_api_key.strip():
        st.error("Please enter Groq API key")

    elif uploaded_file is None:
        st.error("Please upload a video")

    else:
        try:
            with st.spinner("Processing..."):

                # -------------------- SAVE VIDEO --------------------
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_file.read())
                    video_path = tmp.name

                # -------------------- LOAD MODEL --------------------
                model = load_whisper()

                # -------------------- TRANSCRIBE --------------------
                st.info("🔊 Transcribing with Whisper...")
                result = model.transcribe(video_path)
                transcript = result["text"]

                # -------------------- CLEAN FILE --------------------
                os.remove(video_path)

                # -------------------- SPLIT --------------------
                chunks = chunk_text(transcript)

                # -------------------- LLM --------------------
                llm = ChatGroq(
                    model_name="llama-3.3-70b-versatile",
                    groq_api_key=groq_api_key,
                    streaming=False
                )

                # -------------------- SUMMARIZE --------------------
                st.info("Summarizing...")

                partial_summaries = []
                for chunk in chunks:
                    res = llm.invoke(
                        f"Summarize this meeting transcript clearly:\n{chunk}"
                    )
                    partial_summaries.append(res.content)

                final = llm.invoke(
                    "Combine these into a final structured meeting summary:\n"
                    + "\n".join(partial_summaries)
                )

                # -------------------- OUTPUT --------------------
                st.success("Summary Ready")
                st.write(final.content)

        except Exception as e:
            st.error(f"Error: {e}")