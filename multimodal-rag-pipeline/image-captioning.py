import os
from google import genai
from dotenv import load_dotenv

# Loading env variables 
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
prompt = os.getenv("PROMPT")
client = genai.Client(api_key=gemini_api_key)

def image_to_text(path):
    
    uploaded_file = client.files.upload(file=path)

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=[
            {"type": "text", "text": prompt},
            {
                "type": "image",
                "uri": uploaded_file.uri,
                "mime_type": uploaded_file.mime_type
            }
        ]
    )

    return interaction.output_text
