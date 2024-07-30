import speech_recognition as sr
import webbrowser 
import pyttsx3
import musicLibrary
import time
import os
import requests #library to fetch the api and access the methods in it
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import pyaudio
import wave

# Load environment variables from .env file
load_dotenv() 

news_api = os.environ.get("NEWS_API_KEY") 
url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}'

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

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
    
    
    
    
    
def record_audio(output_filename, record_seconds=5, sample_rate=44100, chunk_size=1024):
    audio_format = pyaudio.paInt16  # 16-bit resolution
    channels = 1  # Mono

    audio = pyaudio.PyAudio()

    # Start Recording
    stream = audio.open(format=audio_format, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk_size)
    print("Recording...")
    frames = []

    for _ in range(0, int(sample_rate / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished recording.")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def take_command(): # also returns the text from the audio
   
    record_audio('command.wav')
    AUDIO_FILE = "command.wav"
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        return response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        print(f"Exception: {e}")



if __name__=='__main__': 
    
    # call_out = ["dexter", "desktop", "next", "extra", "dex", "desk"]
    speak("Initializing Dexter...")
    greetUser()
    while True:
        try:
            trigger_word = take_command()
            print(trigger_word)
            if "dexter" in trigger_word.lower():
                speak("Sir")
                command = take_command()
                if "exit" in command.lower():
                    speak("Goodbye Sir!")
                    break
                else:
                    processCommand(command)
            else:
                speak("I am not activated. Please say Dexter to activate me.")
        except Exception as e:
            print("Error while Parsing", e)