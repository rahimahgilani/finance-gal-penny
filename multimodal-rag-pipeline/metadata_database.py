import os, psycopg2
from datetime import date
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

# Open a cursor to perform database operations
connection = psycopg2.connect(db_url)
cursor = connection.cursor()

# Create documents table
create_documents = """
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    filename VARCHAR(100), 
    file_type VARCHAR(100), 
    s3_path VARCHAR(100), 
    upload_date DATE, 
    status VARCHAR
);
"""
cursor.execute(create_documents)

# Create chunks table
create_chunks = """
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES documents(id), 
    chunk_type VARCHAR(100), 
    content_text TEXT,
    page_number INT, 
    image_s3_path VARCHAR(100), 
    faiss_index_id INT
);
"""

cursor.execute(create_chunks)

connection.commit()

# SQL INSERT statement
insert_document = """
INSERT INTO documents (user_id, filename, file_type, s3_path, upload_date, status)
VALUES (%s, %s, %s, %s, %s, %s);
"""

cursor.execute(
    insert_document,
    (user_id, filename, file_type, s3_path, date.today())
)

# SQL INSERT statement
insert_chunk = """
INSERT INTO chunks (document_id, chunk_type, content_text, page_number, image_s3_path, faiss_index_id)
VALUES (%s, %s, %s, %s, %s, %s);
"""

cursor.execute(
    insert_chunk,
    (document_id, chunk_type, content_text, page_number, image_s3_path, faiss_index_id)
)

def update_s3_path(document_id, s3_path):
    sql = """
    UPDATE documents
    SET s3_path = %s
    WHERE id = %s;
    """

    cursor.execute(
        update_s3_path,
        (document_id, s3_path)
    )
    connection.commit()

def update_status(document_id, status):
    sql = """
    UPDATE documents
    SET status = %s
    WHERE id = %s;
    """

    cursor.execute(
        update_status,
        (document_id, s3_path)
    )
    connection.commit()