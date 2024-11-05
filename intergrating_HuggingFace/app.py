import validators, streamlit as st 
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser

#streamlit app
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')


#get the Groq API Key 
with st.sidebar:
    hf_api_key = st.text_input('HuggingFace API Token', value='', type='password')
    
generic_url = st.text_input('URL', label_visibility='collapsed')

#gemma model using Groq API

repo_id = 'mistralai/Mistral-7B-Instruct-v0.2'

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    model_kwargs={
        'max_length': 128,
        'token': hf_api_key
    },
    temperature=0.7,
)

prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

if st.button('Summarize the content from YT or Website'):
    #Validate all the inputs
    if not hf_api_key.strip() or not generic_url.strip():
        st.error('Please provide the information to get started')
elif not validators.url(generic_url):
    st.error('Please enter a valid Url. It can may be  YT video or web url')

else:
    try:
        with st.spinner('Waiting...'):
            if 'youtube.com' in generic_url:
                loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
            else:
                loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                
            docs = loader.load()
            parser = StrOutputParser()
            
            #chain for summarize
            chain = load_summarize_chain(llm, chain_type='stuff', prompt=prompt)
            output_summary = chain.run(docs)
            st.write(output_summary)
            
            st.success(output_summary)
    except Exception as e:
        st.exception(f'Exception: {e}')


