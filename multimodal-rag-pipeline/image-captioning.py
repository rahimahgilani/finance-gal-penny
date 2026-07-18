from google import genai

def image_to_text(path):
    client = genai.Client()
    
    uploaded_file = client.files.upload(file=path)

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=[
            {"type": "text", "text": "Caption this image."},
            {
                "type": "image",
                "uri": uploaded_file.uri,
                "mime_type": uploaded_file.mime_type
            }
        ]
    )
