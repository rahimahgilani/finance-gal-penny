import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from prompts import FOLLOW_UP_PROMPT
from parser import analyse_expenses

## load dotenv file to use the API key stored in it
load_dotenv()

## connect to Groq API
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

## debugging statement
## print(os.getenv("GROQ_API_KEY"))

### ---------------------------------------------- ###
### --------------- USER INTERFACE --------------- ###
### ---------------------------------------------- ###

## Set page title, icon, and layout
st.set_page_config(page_title="Penny - Your Finance Coach", page_icon="💰", layout="centered")

## Styles with headings and a retro pixel font
# put this at the top of your app, before st.html
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        .pixel-wrap { padding: 1.5rem 1rem; text-align: center; }
        .pixel-title {
            font-family: 'Press Start 2P', monospace;
            font-size: clamp(12px, 2.5vw, 20px);
            color: #ffffff;
            letter-spacing: 2px;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid #ffffff;
            width: 0;
            display: inline-block;
            animation: type 2.4s steps(30, end) forwards, blink 0.75s step-end infinite;
        }
        .pixel-sub {
            font-family: 'Press Start 2P', monospace;
            font-size: 9px;
            color: #aaaaaa;
            margin-top: 1rem;
            opacity: 0;
            animation: fadein 0.5s ease 2.6s forwards;
            line-height: 2;
        }
        @keyframes type { to { width: 30ch; } }
        @keyframes blink { 50% { border-color: transparent; } }
        @keyframes fadein { to { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

st.html("""
<div class="pixel-wrap">
  <span class="pixel-title">🤑 PENNY - Your Finance Sis</span>
  <p class="pixel-sub">PASTE YOUR MONTHLY EXPENSES BELOW</p>
</div>
""")

temp_dir = 'multimodal-rag-pipeline\content'

with st.form(key="expenses-chat-window"):
    user_text = st.text_area("e.g.\nRent 25000\nGroceries 8000")
    
    submit_button = st.form_submit_button(label="Process Text")

    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "csv", "docx", "image"], accept_multiple_files=False, key="upload-doc")
   
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
## When the user clicks the "Analyse" button, call the analyse_expenses function and display the results
if st.button("Analyse my expenses"):
    if not expenses.strip():
        st.warning("Please paste some expenses first.")
    else:
        with st.spinner("Analysing..."):
            try:
                data = analyse_expenses(expenses)

                st.success("Done! Here's your breakdown.")
                
                # total spend
                st.metric("Total Spend", f"{data['currency']} {data['total']:,}")

                # bar chart
                st.subheader("Spending by category")
                chart_data = {c["name"]: c["amount"] for c in data["categories"]}
                st.bar_chart(chart_data)

                # category breakdown
                st.subheader("Breakdown")
                for cat in data["categories"]:
                    st.write(f"**{cat['name']}** — {data['currency']} {cat['amount']:,} ({cat['percent']}%)")

                # saving tips
                st.subheader("💡 Saving Tips")
                for tip in data["saving_tips"]:
                    st.info(tip)

                # save data for follow-up chat
                st.session_state["expense_data"] = data
                st.session_state["expenses_text"] = expenses

            except Exception as e:
                st.error(f"Something went wrong: {e}")

## If the user has already analysed their expenses, allow them to ask follow-up questions
if "expense_data" in st.session_state:
    st.divider()
    st.subheader("🗨️ Ask a follow-up question")
    question = st.text_input("e.g. How do I reduce my food spend?")

    if st.button("Ask"):
        if question.strip():
            with st.spinner("Thinking..."):
                follow_up_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": FOLLOW_UP_PROMPT},
                        {"role": "user", "content": f"My expense data: {st.session_state['expense_data']}\n\nMy question: {question}"}
                    ]
                )
                answer = follow_up_response.choices[0].message.content
                st.write(answer)