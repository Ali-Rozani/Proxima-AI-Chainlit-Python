import chainlit as ct
from GoogleGeminiLLM import generate

@ct.on_message
async def main(message: ct.Message):
    user_input_text = message.content
    image_data = None

    if message.elements:
        for element in message.elements:
            if element.type == "image":
                image_data = element.content
                break

    response_chunks = generate(user_message=user_input_text, image_data=image_data)
    msg = ct.Message(content="")
    await msg.send()
    for chunk in response_chunks:
        await msg.stream_token(chunk)