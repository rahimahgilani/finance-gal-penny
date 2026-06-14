import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, FOLLOW_UP_PROMPT

# load dotenv file to use the API key stored in it
load_dotenv()

#connect to Groq API
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def analyse_expenses(expenses_text):
    # user --> the text they enter 
    # system --> the prompt that guides the model on how to analyse the expenses and what output format to use
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": expenses_text}
        ]
    )
    
    # the model's response will be in the format specified in the system prompt, but we still need to clean it and convert it from a string to a JSON object
    raw = response.choices[0].message.content
    
    # clean response in case model adds anything before/after JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    # convert json to dict
    return json.loads(raw) 

