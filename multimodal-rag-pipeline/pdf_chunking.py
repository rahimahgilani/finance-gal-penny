import pymupdf
import pandas as pd
import pdfplumber
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

def extract_all_text(pdf_path):
    # Step 1: Open a document
    doc = pymupdf.open(pdf_path)
    extracted_text = []

    # Step 3: Iterate the document pages
    for page_index in range(len(doc)): # iterate over pdf pages
        page = doc[page_index]
        text = page.get_text()

        # Step 4: Call LangChain RecursiveCharacterTextSplitter to split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        # Step 5: Add to dict
        extracted_text.append({
            'page': page_index,
            'chunk_type': 'text',
            'context_text': chunks
        })

    return extracted_text

def extract_all_tables(pdf_path):
    extracted_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables(TABLE_SETTINGS)
                                
            if tables_on_page:
                for table in tables_on_page:
                    if table:
                        table_df = pd.DataFrame(table)
                        extracted_tables.append({
                            'page': pdf.pages.index(page) + 1,
                            'chunk_type': 'table',
                            'context_text': table_df.to_markdown(index=False)
                        })

    return extracted_tables

def extract_all_images(pdf_path):
    doc = pymupdf.open(pdf_path)
    extracted_images = []

    for page_index in range(len(doc)): # iterate over pdf pages
        page = doc[page_index] # get the page
        image_list = page.get_images()

        for image_index, img in enumerate(image_list, start=1): # enumerate the image list
            xref = img[0] # get the XREF of the image
            pix = pymupdf.Pixmap(doc, xref) # create a Pixmap

            if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

            extracted_images.append({
                            'page': page_index,
                            'index': image_index,
                            'chunk_type': 'image',
                            'image_bytes': pix.tobytes("png")
                        })

    return extracted_images