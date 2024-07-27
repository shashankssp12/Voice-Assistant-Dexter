import speech_recognition as sr
import webbrowser #
import pyttsx3
import musicLibrary
import time
import os
import requests #library to fetch the api and access the methods in it
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv() 

news_api = os.environ.get("NEWS_API_KEY") 
url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}'
# --------------

recognizer = sr.Recognizer() #recognizes the audio
engine = pyttsx3.init() #text-to-speech engine



# Function to speak the text
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Function to process the command
def processCommand(command):
    
    if "vs code" in command.lower():
        os.system("code")
    elif "notepad" in command.lower():
        os.system("notepad")
    elif "google" in command.lower():
        webbrowser.open("https://google.com")
    elif "linkedin" in command.lower():
            webbrowser.open("https://linkedin.com")
    elif "coding ninjas" in command.lower():
            webbrowser.open("https://codingninjas.com")
    elif "github" in command.lower():
            webbrowser.open("https://github.com")
    elif "youtube" in command.lower():
            webbrowser.open("https://youtube.com") 
    elif command.lower().startswith("play"):
        song = " ".join(command.lower().split(" ")[1:])
        print(song)
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Song not found in the music library")
    elif "news" in command.lower():
            response = requests.get(url)
            # Fetch the response from the API
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Load the JSON response into a dictionary
                data = response.json()
                # Extract the headlines
                headlines = [article['title'] for article in data['articles'][:5:]]
                # Print the headlines
                for i, headline in enumerate(headlines, start=1):
                    speak(f"{i}. {headline}")
            else:
                speak("Failed to fetch data from the API")
    else: 
        response_ai = processAI(command)
        speak(response_ai) 
    
# Creating OpenAI client and processing the command
def processAI(command):    
    client = OpenAI(
      api_key=os.environ.get("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named Dexter. Give short yet resourceful answers like Alexa , google cloud and jarvis from the iron man picture."},
        {"role": "user", "content": command}
      ]
    )
    return completion.choices[0].message.content

def greetUser():
    hour = int(time.strftime("%H"))
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("The current time is " + time.strftime("%I:%M %p"))
    speak("How may I help you today?")

def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        
        # recognizer.pause_threshold = 1 #seconds of non-speaking audio before a phrase is considered complete 
    
        audio = recognizer.listen(source , timeout=2 #
                                  , phrase_time_limit=2 #
                                  ) #listening to the source
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print("You said: "+query)            
        except Exception as e:
            print("Say that again please...")
            print(e)
            
        return query


if __name__=='__main__': 
    speak("Initializing Dexter...")
    greetUser()
    while True:
        try:
            trigger_word = takeCommand().lower()
            if "dexter" or "desktop" or "next" or "extra" or "dex" or "desk" in trigger_word.lower(): #I havent added 'text' or 'start' or 'xender' as the trigger words , but still it is working and I am not able to understand why 
                speak("Sir")
                command = takeCommand()
                if "exit" in command.lower():
                    speak("Goodbye Sir!")
                    break
                else:
                    processCommand(command)
            else:
                speak("I am not activated. Please say Dexter to activate me.")
                
        except Exception as e:
            print("Error while Parsing" , e)
