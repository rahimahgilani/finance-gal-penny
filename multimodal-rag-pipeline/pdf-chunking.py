# from unstructured.partition.pdf import partition_pdf


# def partition_and_chunk_pdf(file_path):
#     chunks = partition_pdf(
#         filename=file_path,
#         infer_tables_structure=True,           # Extract tables with structure
#         strategy='hi_res',                     # Mandatory to infer tables
#         extract_image_block_types=["Image"],   # Extract images
#         extract_image_block_to_payload=True,   # Extract base64 object of the image
#         chunking_strategy="by_title",          # Chunking strategy
#         max_characters=2000,                   # Max characters per chunk
#         combine_text_under_n_chars=500,        # Combine small text blocks
#         new_after_n_chars=6000,                # New chunk after this many characters
#     )
#     return chunks

# def get_table(chunks):
#     tables = []
#     for chunk in chunks:
#         for el in chunk.metadata.orig_elements:
#             if 'Table' in str(type(el)):
#                 print(el.to_dict())
#                 tables.append(el)
#     return tables

# def save_texts(chunks):
#     texts = [chunk for chunk in chunks if 'CompositeElement' in str(type(chunk))]
#     return texts

# def get_image_base64(chunks):
#     image_b64 = []
#     for chunk in chunks:
#         chunk_el = chunk.metadata.orig_elements
#         for el in chunk_el:
#             if 'Image' in str(type(el)):
#                 image_b64.append(el.metadata.image_base64)
#     return image_b64