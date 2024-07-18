from openai import OpenAI
import os 

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual like assistant like Alexa , google cloud and jarvis"},
    {"role": "user", "content": "What is coding?"}
  ]
)

print(completion.choices[0].message.content)