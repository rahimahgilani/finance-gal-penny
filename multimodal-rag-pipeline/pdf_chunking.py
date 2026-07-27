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

def table_to_markdown(table_df):
    # Convert DataFrame to Markdown
    markdown_table = table_df.to_markdown(index=False)

    # Save the Markdown table locally
    with open("table-output.md", "w", encoding="utf-8") as file:
        file.write(markdown_table)

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
                            'chunk_type': table,
                            'content_text': table_to_markdown(table_df)
                        })

    return extracted_tables

def extract_all_images(pdf_path):
    doc = pymupdf.open(pdf_path)
    
    for page_index in range(len(doc)): # iterate over pdf pages
        page = doc[page_index] # get the page
        image_list = page.get_images()

        # print the number of images found on the page
        if image_list:
            print(f"Found {len(image_list)} images on page {page_index}")
        else:
            print("No images found on page", page_index)

        for image_index, img in enumerate(image_list, start=1): # enumerate the image list
            xref = img[0] # get the XREF of the image
            pix = pymupdf.Pixmap(doc, xref) # create a Pixmap

            if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

            pix.save(f"page_{page_index}_image_{image_index}.png") # save the image as png
            pix = None
