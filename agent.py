
import os
import base64
from io import BytesIO

from groq import Groq
from PIL import Image
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Connect to Groq
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env file")

client = Groq(api_key=api_key)

# AI model
MODEL_NAME = "qwen/qwen3.8-27b"


# Main image analysis function
def analyze_image(image, prompt):

    # Convert image into RGB format
    image = image.convert("RGB")

    # Convert image into Base64
    buffer = BytesIO()
    image.save(buffer, format="JPEG")

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    image_url = (
        f"data:image/jpeg;base64,{encoded_image}"
    )

    # Send image and prompt to AI model
    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful multimodal AI agent. "
                    "Analyze images carefully and answer "
                    "the user's questions clearly. "
                    "Do not invent information."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],

        max_completion_tokens=1024
    )

    # Extract AI response
    answer = response.choices[0].message.content

    return answer
