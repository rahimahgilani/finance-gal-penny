from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.messages import HumanMessage

load_dotenv()

def rag_chain_pipeline(vector_store, question, filename):
    # Step 1: Querying the collection by turning it into a retriever
    retriever = vector_store.as_retriever(search_kwargs={"filter": {"source": filename}})

    text = retriever.invoke(question)

    # print(f"Retrieved text: {text}")
    # print(f"Number of retrieved documents: {len(text)}")

    # Step 2: Convert the retrieved documents into a single string
    singleString = " ".join([item.page_content for item in text])

    # print(f"Single string: {singleString}")

    # Step 3: Setting up ChatGroq
    llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

    # Step 4: Building a simple prompt template
    message = HumanMessage(
        content=[
            {"type": "text", "text": singleString},
            {"type": "text", "text": question},
        ]
    )

    response = llm.invoke([message])
    return response.content
