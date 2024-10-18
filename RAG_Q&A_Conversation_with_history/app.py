import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

#set up streamlit
st.title('Conversational RAG with pdf uploads and chat history')
st.write('Upload your pdf and chat with their content')

#input the Groq API key
api_key = st.text_input('Enter your Groq API key:', type='password')

#Check if groq api key is provided
if api_key:
    llm = ChatGroq(model_name="Gemma2-9b-It", groq_api_key=api_key)
    
    #chat interface
    session_id = st.text_input('Session ID', value='default_session')
    
    #statefully manage chat history
    if 'store' not in st.session_state:
        st.session_state.store = {}
        
    #process uploaded PDF
    uploaded_files = st.file_uploader("Choose a PDF file", type='pdf', accept_multiple_files=True)
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            temp_pdf = f"RAG_Q&A_Conversation_with_history/temp_{uploaded_file.name}"
            with open(temp_pdf, 'wb') as file:
                file.write(uploaded_file.getvalue())
                file_name = uploaded_file.name
            
            #load the pdf file and save to documents    
            loader = PyPDFLoader(temp_pdf)
            docs = loader.load()
            documents.extend(docs)
            
            # #delete the temp file
            # os.remove(temp_pdf)
            
        #split and create embeddings for the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
        retriever = vector_store.as_retriever()            
        
        contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder('chat_history'),
                ('human', '{input}'),
            ]
        )
        
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        
        #Answer question
        system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
        
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder('history_chat'),
                ('user', '{input}'),
            ]
        )
        
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        
        def get_session_history(session_id:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
            return st.session_state.store[session_id]
        
        
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain, get_session_history,
            input_messages_key="input",
            history_messages_key="history_chat",
            output_messages_key="answer"
        )
        
        user_input = st.text_input("Your question:")
        if user_input:
            print("A1111111111111111111111111111") 
            session_history = get_session_history(session_id)
            print("A22222222222222222222222222222222222222222222") 
            response = conversational_rag_chain.invoke(
                {'input': user_input},
                config={
                    'configurable': {'session_id': session_id}
                }, 
            )
            
            st.write(st.session_state.store)
            st.write("Assitant:", response['answer'])
            st.write("Chat History:", session_history.messages)
            
else:
    st.write("Please enter the GRoq API Key")