import streamlit as st
import os
import openai
import time

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv

load_dotenv()

#Embedding vector
def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings=OpenAIEmbeddings()
        st.session_state.loader=PyPDFDirectoryLoader("chatbot_read_paper/research_papers") 
        st.session_state.docs=st.session_state.loader.load() 
        
        #check if document loaded sucessfully 
        if not st.session_state.docs:
            st.write("No documents found in the 'research_papers' directory.")
            return
        
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
    else:
        st.write("Vector embeddings are already created.")
        
        

#load the GROQ API key
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(model_name="Llama3-8b-8192", groq_api_key=groq_api_key)

prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate respone based on the question
    <context>
    {context}
    <context>
    Question:{input}

    """

)

#App title
st.title("RAG Document Q&A with Groq and Llama3")

if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Vector Database ist ready")
    
    #create retrieval chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    st.session_state.retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
user_prompt = st.text_input("Enter your query from the research paper")

if user_prompt:
    start = time.process_time()
    response = st.session_state.retrieval_chain.invoke({"input":user_prompt})
    print(f"Response time: {time.process_time() - start}")
    
    st.write(response['answer'])
    
    #with a streamlit expander
    if 'context' in response and response['context']:
            with st.expander("Document similarity search"):
                for i, doc in enumerate(response['context']):
                    st.write(doc.page_content)
                    st.write('-------------------------------------')
    else:
        st.write("No relevant documents were found.")