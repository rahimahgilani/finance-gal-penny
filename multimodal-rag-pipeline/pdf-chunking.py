import pymupdf
import pdfplumber
import pandas as pd 
from langchain_text_splitters import RecursiveCharacterTextSplitter

TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_tolerance": 5,
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 2,
    "min_words_horizontal": 1,
    "text_keep_blank_chars": True,
}

def pdf_chunking(filename):
    # Step 1: Open a document
    doc = pymupdf.open(filename)

    if doc:
        print(f"Document opened successfully: {doc}")
    else:
        print("Failed to open the document.")

    # Step 2: Extract text from a PDF
    out = open("output.txt", "wb")

    # Step 3: Iterate the document pages
    for page in doc:
        # gets plain text
        text = page.get_text().encode("utf8")
        # write the text of the page 
        out.write(text)
        # write page delimiter
        out.write(bytes((12,))) 
    out.close()

    # print("Iterated through the document and extracted text successfully.")

    # Step 4: Call LangChain RecursiveCharacterTextSplitter to split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(open("output.txt", "r", encoding="utf8").read())
    # print(f"Number of chunks: {len(chunks)}")
    # print(chunks[0]) # print the first chunk
    return chunks

def extract_all_tables(pdf_path):
    extracted_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables(TABLE_SETTINGS)

            if tables_on_page:
                for table in tables_on_page:
                    if table:
                        extracted_tables.append({
                            'page': pdf.pages.index(page) + 1,
                            'data': table
                        })
    
    return extracted_tables
