import requests
import streamlit as st

def get_groq_response(input_text):
    # Construct the request body dynamically
    json_body = {
        "input": {
            "language": "French",  # Language as per your Langchain model
            "text": input_text      # Dynamic user input
        },
        "config": {},
        "kwargs": {}
    }
    
    try:
        # Send the POST request to the FastAPI server
        response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Extract the output from the response
        response_data = response.json()
        return response_data.get('output', 'No output found')  # Adjust this key to match your response structure
    except requests.exceptions.RequestException as e:
        # Handle any request errors
        st.error(f"Request failed: {e}")
        return None

## Streamlit app
st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to convert to French")

if input_text:
    response = get_groq_response(input_text)
    if response:
        st.write("Translated text:", response)
