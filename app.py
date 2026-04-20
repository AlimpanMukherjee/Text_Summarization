# import streamlit as st
# import validators
# from langchain.prompts import PromptTemplate 
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

# st.title("Website or Youtube video Summarizer")


# def clean_text(docs):
#     for doc in docs:
#         doc.page_content = doc.page_content.encode("utf-8", "ignore").decode("utf-8")
#     return docs


# ## Get the Groq API
# with st.sidebar:
#     groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# generic_url=st.text_input("Enter your URL",label_visibility="collapsed")
# llm=ChatGroq(
#     model_name="llama-3.3-70b-versatile",
#     groq_api_key=groq_api_key
# )
# prompt_template="""
# provide a summary for the following text: {text}
# """

# if st.button("Summarize"):
#     if not groq_api_key.strip() or not generic_url.strip():
#         st.error("Please provide the information to get started")
#     elif not validators.url(generic_url):
#         st.error("Please enter a valid URL")
#     else:
#         try:
#             with st.spinner("Summarizing..."):
#                 if "youtube.com" in generic_url:
#                     loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True,language=["hi", "en"])
#                 else:
#                     loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}) 
#                 data = loader.load()
#                 data = clean_text(data)

#                 ## Chain for summarization
#                 chain=load_summarize_chain(llm,chain_type="stuff",prompt=PromptTemplate(template=prompt_template,input_variables=["text"]))
#                 output_summary=chain.run(data)
#                 st.success(output_summary)
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# import validators,streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader


# ## sstreamlit APP
# st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
# st.title("🦜 LangChain: Summarize Text From YT or Website")
# st.subheader('Summarize URL')



# ## Get the Groq API Key and url(YT or website)to be summarized
# with st.sidebar:
#     groq_api_key=st.text_input("Groq API Key",value="",type="password")

# generic_url=st.text_input("URL",label_visibility="collapsed")

# ## Gemma Model USsing Groq API
# llm =ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)

# prompt_template="""
# Provide a summary of the following content in 300 words:
# Content:{text}

# """
# prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

# if st.button("Summarize the Content from YT or Website"):
#     ## Validate all the inputs
#     if not groq_api_key.strip() or not generic_url.strip():
#         st.error("Please provide the information to get started")
#     elif not validators.url(generic_url):
#         st.error("Please enter a valid Url. It can may be a YT video utl or website url")

#     else:
#         try:
#             with st.spinner("Waiting..."):
#                 ## loading the website or yt video data
#                 if "youtube.com" in generic_url:
#                     loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
#                 else:
#                     loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
#                                                  headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
#                 docs=loader.load()

#                 ## Chain For Summarization
#                 #chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
#                 chain=load_summarize_chain(llm=llm,chain_type="refine",verbose=True)

#                 output_summary=chain.run(docs)

#                 st.success(output_summary)
#         except Exception as e:
#             st.exception(f"Exception:{e}")
                    


import streamlit as st
import validators
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.title("Website Summarizer")

# -------------------- API KEY --------------------
with st.sidebar:
    groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# -------------------- URL INPUT --------------------
generic_url = st.text_input("Enter your URL", label_visibility="collapsed")

# # -------------------- LLM --------------------
# llm = ChatGroq(
#     model_name="llama-3.3-70b-versatile",
#     groq_api_key=groq_api_key,
#     streaming=False  # stability
# )

# -------------------- CLEAN TEXT --------------------
def clean_text(docs):
    for doc in docs:
        doc.page_content = doc.page_content.encode("utf-8", "ignore").decode("utf-8")
    return docs


# -------------------- MAIN BUTTON --------------------
if st.button("Summarize"):

    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide API key and URL")

    elif not validators.url(generic_url):
        st.error("Please enter a valid URL")

    else:
        try:
            with st.spinner("Processing..."):

                # -------------------- LOAD DATA --------------------
                # if "youtube.com" in generic_url or "youtu.be" in generic_url:
                #     loader = YoutubeLoader.from_youtube_url(
                #         generic_url,
                #         add_video_info=True,
                #         language=["hi", "en"]
                #     )
                # else:
                llm = ChatGroq(
                    model_name="llama-3.3-70b-versatile",
                    groq_api_key=groq_api_key,
                    streaming=False  # stability
                )
                loader = UnstructuredURLLoader(
                    urls=[generic_url],
                    ssl_verify=False,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                data = loader.load()

                # -------------------- CLEAN TEXT --------------------
                data = clean_text(data)

                # -------------------- SPLIT TEXT (IMPORTANT) --------------------
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=2000,
                    chunk_overlap=200
                )

                docs = text_splitter.split_documents(data)

                # -------------------- SUMMARIZATION --------------------
                chain = load_summarize_chain(
                    llm,
                    chain_type="map_reduce"   # IMPORTANT for large data
                )

                result = chain.invoke(docs)

                st.success(result["output_text"])

        except Exception as e:
            st.error(f"Error: {e}")