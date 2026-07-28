from datetime import date
from pdf_chunking import *
from s3_aws import upload_bytes, upload_file
from metadata_database import *

def ingest_pdf(pdf_path, user_id):
    filename = os.path.basename(pdf_path)

    # Step 1: Insert document row, get back the document_id
    document_id = insert_document(
        user_id=user_id,
        filename=filename,
        file_type='pdf',
        s3_path='pending',   
        upload_date=date.today(),
        status='processing'
    )

    # Step 2: Build S3 path now that you have document_id
    s3_key = f"{user_id}/{document_id}/{filename}"

    # Step 3: Upload PDF to S3 using structured path
    upload_file(pdf_path, object_name=s3_key)

    # Step 4: Update the document row with the real S3 path
    update_s3_path(document_id, s3_key)

    # Step 5: Extract and insert chunks
    text_chunks = extract_all_text(pdf_path)
    table_chunks = extract_all_tables(pdf_path)
    image_chunks = extract_all_images(pdf_path)

    # Step 6: Insert each chunk type (you'll build these next)
    for chunk in text_chunks:
        insert_chunk(document_id, 'text', chunk['context_text'], chunk['page'],  image_s3_path=None, faiss_index_id=None)

    for chunk in table_chunks:
        insert_chunk(document_id, 'table', chunk['context_text'], chunk['page'], image_s3_path=None, faiss_index_id=None)

    for chunk in image_chunks:
        s3_image_key = f"{user_id}/{document_id}/images/page_{chunk['page']}_img_{chunk['index']}.png"
        upload_bytes(chunk['image_bytes'], s3_image_key)
        insert_chunk(document_id, 'image', None, chunk['page'], image_s3_path=s3_image_key, faiss_index_id=None)

    # Step 7: Mark document as complete
    update_status(document_id, 'complete')
    print("Document Chunking and Uploading Complete!")

