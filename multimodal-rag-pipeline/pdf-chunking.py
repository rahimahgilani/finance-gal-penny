import pymupdf

def pdf_chunking(file):
    doc = pymupdf.open(file)

    # Extracting text from a pdf
    out = open("output.txt", "wb")

    # Iterate the document pages
    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,))) 
    out.close()

    # Call LangChain RecursiveCharacterTextSplitter to split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(open("output.txt", "r", encoding="utf8").read())
    return chunks
