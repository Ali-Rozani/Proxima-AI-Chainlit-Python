import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

def generate(user_message: str, image_data: str = None):
    client = genai.Client(
        api_key=API_KEY,
    )

    model = "gemini-2.5-flash-preview-04-17"

    user_parts = []

    combined_text = f"YOUR NAME IS PROXIMA AI AND YOU ARE A PERSONAL ASSISTANT.\n\n{user_message}"

    user_parts.append(types.Part.from_text(text=combined_text))

    if image_data:
        user_parts.append(
            types.Part.from_data(
                inline_data=types.Blob(
                    mime_type='image/jpeg',
                    data=base64.b64decode(image_data)
                )
            )
        )

    contents = [types.Content(role="user", parts=user_parts)]

    tools = [
        types.Tool(
            function_declarations=[
            ])
    ]

    generate_content_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_LOW_AND_ABOVE", # Corrected typo here
            ),
        ],
        tools=tools,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        yield chunk.text if chunk.function_calls is None else str(chunk.function_calls[0])

if __name__ == "__main__":
    test_message_text = "Tell me a joke."
    for response_chunk in generate(test_message_text):
        print(response_chunk, end="")
    print("\n")