import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise SystemExit("No se encontró ANTHROPIC_API_KEY en el archivo .env")

client = Anthropic(api_key=api_key)

respuesta = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": "Escribe un saludo corto y entusiasta para el Bootcamp AGENTIC.",
        }
    ],
)

print(respuesta.content[0].text)
