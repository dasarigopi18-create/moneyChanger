from typing import Tuple, Dict

import dotenv
import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv(override=True)
EXCHANGE_RATE_API = os.getenv('EXCHANGE_API_KEY')

import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API}/pair/{base}/{target}/{amount}'
    respose = json.loads(requests.get(url).text)
    return (base, target, amount, f'{respose["conversion_result"]:.2f}')

print(get_exchange_rate('USD', 'GBP', 250))

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )

        
    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return response.choices[0].message.content
def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")

    # Title of the app
st.title("MultiLingual Money Changer")

# Checkbox for user input
input_checkbox = st.checkbox("Enter Amount and Currency")

# Text input field
if input_checkbox:
    user_input = st.text_input("Enter the amount and Currency:")
    
    # Button to submit the entered amount
    if st.button("Submit"):
        # Display the entered amount below the text box
        st.write(call_llm(user_input))