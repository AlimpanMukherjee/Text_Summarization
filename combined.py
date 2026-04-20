# import streamlit as st
# import os
# import tempfile
# import shutil

# # -------------------- FIX FFMPEG PATH --------------------
# os.environ["PATH"] += r";C:\Users\KIIT0001\Desktop\losslesscut\resources"

# # -------------------- IMPORTS --------------------
# # -------------------- IMPORTS --------------------
# import whisper
# import validators
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.docstore.document import Document


# st.title("Summarizer")

# # -------------------- API KEY --------------------
# with st.sidebar:
#     groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# #----------------------MODE SELECTION---------------------
# mode = st.selectbox("Select mode", ["Text", "URL", "Video"])

# #----------------------COMMON FUNCTION----------------------
# def clean_text(docs):
#     for doc in docs:
#         doc.page_content=doc.page_content.encode("utf-8","ignore").decode("utf-8")
#     return docs

# def chunk_docs(docs):
#     splitter=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=200)
#     return splitter.split_documents(docs)

# @st.cache_resource
# def load_whisper():
#     return whisper.load_model("base")  

# #----------------------INPUT SECTION----------------------
# if mode=="URL":
#     generic_url=st.text_input("Enter URL")
# elif mode=="Video":
#     uploaded_file=st.file_uploader(
#         "Upload a video file",
#         type=["mp4", "mov", "avi", "mkv"]
#     )
# elif mode=="Text":
#     input_text=st.text_area("Paste your text here",height=200)

# #----------------------MAIN BUTTON----------------------
# if st.button("Summarize"):
#     if not groq_api_key.strip():
#         st.error("Please enter Groq API key")
#         st.stop()
# #----------------------INIT LLM------------------------------
#     llm=ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)
#     try :
#         with st.spinner("Processing"):

#             if mode=="URL":
#                 if not generic_url or  not validators.url(generic_url):
#                     st.error("Enter Valid URL")
#                     st.stop()

#                 loader=UnstructuredURLLoader(
#                     urls=[generic_url],
#                     ssl_verify=False,
#                     headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
#                 )
#                 data=loader.load()
#                 data=clean_text(data)
#                 docs=chunk_docs(data)

#             elif mode=="Video":
#                 if uploaded_file is None:
#                     st.error("Please upload a video")
#                     st.stop()
#                 with tempfile.NamedTemporaryFile(delete=False,suffix=".mp4") as tmp:
#                     tmp.write(uploaded_file.read())
#                     video_path=tmp.name
#                 model=load_whisper()
#                 st.info("🔊 Transcribing...")
#                 result=model.transcribe(video_path,task="translate")
#                 transcript=result["text"]
#                 os.remove(video_path)
#                 docs=chunk_docs([Document(page_content=transcript)])
                
#             elif mode=="Text":
#                 if not input_text.strip():
#                     st.error("Please enter text")
#                     st.stop()
#                 docs=chunk_docs([Document(page_content=input_text)])
#     #----------------------SUMMARIZE--------------------------------
#             chain=load_summarize_chain(llm,chain_type="map_reduce",verbose=True)
#             output_summary=chain.run(docs)
#             st.success(output_summary)
#             st.balloons()

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

import streamlit as st
import os
import tempfile
import shutil

# -------------------- FIX FFMPEG PATH --------------------
os.environ["PATH"] += r";C:\Users\KIIT0001\Desktop\losslesscut\resources"

# -------------------- IMPORTS --------------------
import whisper
import validators
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

st.title("Summarizer")

# -------------------- API KEY --------------------
with st.sidebar:
    groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# ----------------------MODE SELECTION---------------------
mode = st.selectbox("Select mode", ["Text", "URL", "Video"])

# ----------------------COMMON FUNCTION----------------------
def clean_text(docs):
    for doc in docs:
        doc.page_content = doc.page_content.encode("utf-8", "ignore").decode("utf-8")
    return docs

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    return splitter.split_documents(docs)

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

# ----------------------INPUT SECTION----------------------
if mode == "URL":
    generic_url = st.text_input("Enter URL")

elif mode == "Video":
    uploaded_file = st.file_uploader(
        "Upload a video file",
        type=["mp4", "mov", "avi", "mkv"]
    )

elif mode == "Text":
    input_text = st.text_area("Paste your text here", height=200)

# ----------------------MAIN BUTTON----------------------
if st.button("Summarize"):
    if not groq_api_key.strip():
        st.error("Please enter Groq API key")
        st.stop()

    llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

    try:
        with st.spinner("Processing"):

            # ---------------- URL ----------------
            if mode == "URL":
                if not generic_url or not validators.url(generic_url):
                    st.error("Enter Valid URL")
                    st.stop()

                loader = UnstructuredURLLoader(
                    urls=[generic_url],
                    ssl_verify=False,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                data = loader.load()
                data = clean_text(data)
                docs = chunk_docs(data)

            # ---------------- VIDEO ----------------
            elif mode == "Video":
                if uploaded_file is None:
                    st.error("Please upload a video")
                    st.stop()

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_file.read())
                    video_path = tmp.name

                model = load_whisper()

                
                st.info("🔊 Transcribing...")

                result = model.transcribe(video_path, task="translate")
                transcript = result["text"]

                os.remove(video_path)

                docs = chunk_docs([Document(page_content=transcript)])

            # ---------------- TEXT ----------------
            elif mode == "Text":
                if not input_text.strip():
                    st.error("Please enter text")
                    st.stop()

                docs = chunk_docs([Document(page_content=input_text)])

            
            st.info("🧠 Summarizing...")

            # ---------------- SUMMARIZE ----------------
            map_prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                Summarize the following text in concise bullet points:{text}
                """
            )
            combine_prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                Create a final structured and detailed summary with key insights:{text}
                """
            )
            chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt,combine_prompt=combine_prompt,verbose=True)
            output_summary = chain.run(docs)

            st.success(output_summary)
            st.balloons()

            # download button
            st.download_button(
                "Download Summary",
                output_summary,
                file_name="summary.txt"
            )

            # transcript viewer (only for video)
            if mode == "Video":
                with st.expander("📄 View Full Transcript"):
                    st.write(transcript)

    except Exception as e:
        st.error(f"An error occurred: {e}")