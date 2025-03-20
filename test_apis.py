import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from deepgram import DeepgramClient

load_dotenv()

def test_news_api():
    print("\n--- Testing News API ---")
    news_api = os.environ.get("NEWS_API_KEY")
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}'
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ News API is working!")
        print(f"Sample headline: {response.json()['articles'][0]['title']}")
    else:
        print(f"❌ News API error: {response.status_code}")
        print(response.text)

def test_openai_api():
    print("\n--- Testing OpenAI API ---")
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello as Dexter"}]
        )
        print("✅ OpenAI API is working!")
        print(f"Response: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")

def test_deepgram_api():
    print("\n--- Testing Deepgram API ---")
    try:
        deepgram = DeepgramClient(api_key=os.environ.get("DEEPGRAM_API_KEY"))
        # Just test connection - no actual transcription
        if deepgram:
            print("✅ Deepgram client created successfully!")
    except Exception as e:
        print(f"❌ Deepgram API error: {e}")

if __name__ == "__main__":
    print("Starting API tests...\n")
    test_news_api()
    test_openai_api() 
    test_deepgram_api()
    print("\nAPI tests completed!")