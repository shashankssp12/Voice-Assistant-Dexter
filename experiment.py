
import webbrowser 
import pyttsx3
import musicLibrary
import os
import requests 
from dotenv import load_dotenv
import time
import asyncio
import pyaudio
import wave
import logging
import pygame
# from playAudio import play_audio
from deepgram.utils import verboselogs
# from TTS import save_response_as_audio, play_audio
from openai import OpenAI
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
    SpeakOptions,
)
load_dotenv()

# for playing audio: 
from pydub import AudioSegment
from pydub.playback import play
#--------------------------------



news_api = os.environ.get("NEWS_API_KEY") 
url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}'
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")
DEEPGRAM_URL = "https://api.deepgram.com/v1/speak?model=aura-orion-en"

is_finals = []



def save_response_as_audio(response):
    print("Dexter: " + response)
    payload = {
        "text": response 
            }

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }

    audio_file_path = "output_TTS.wav"  # Path to save the audio file

    with open(audio_file_path, 'wb') as file_stream:
        response = requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file_stream.write(chunk) # Write each chunk of audio data to the file

    print("Audio download complete")
    # Play the audio file
    audio = AudioSegment.from_file(audio_file_path)
    play(audio)

    # Delete the audio file after playback
    os.remove(audio_file_path)
    print("Audio file deleted")


def process_input():
    
    try:
        deepgram: DeepgramClient = DeepgramClient()

        dg_connection = deepgram.listen.websocket.v("1")

        def on_open(self, open, **kwargs):
            print("Connection Open")

        def on_message(self, result, **kwargs):
            global is_finals
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                # Speech Final means we have detected sufficent silence to consider this end of speech
                is_finals.append(sentence)
                if result.speech_final:
                    utterance = " ".join(is_finals)
                    
                    print(f"User: {utterance}")
                    # processAI(utterance)
                    # speak(utterance)
                    if "exit" in utterance.lower():
                        speak_advance("Goodbye Sir!")
                        return
                    else:
                      processAI(utterance)
                    is_finals = []
                else:
                    # These are useful if you need real time captioning and update what the Interim Results produced
                    print(f"Is Final: {sentence}")

        def on_metadata(self, metadata, **kwargs):
            print(f"Metadata: {metadata}")

        def on_close(self, close, **kwargs):
            print("Connection Closed")

        def on_error(self, error, **kwargs):
            print(f"Handled Error: {error}")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"Unhandled Websocket Message: {unhandled}")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)
    
        options: LiveOptions = LiveOptions(
            model="nova-2",
            language="en-IN",
            # Apply smart formatting to the output
            smart_format=True,
            # Raw audio format details
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
            # Time in milliseconds of silence to wait for before finalizing speech
            endpointing=300,
        )

        addons = {
            # Prevent waiting for additional numbers
            "no_delay" : "true"
        }

        print("\n\nListening...")
        if dg_connection.start(options, addons=addons) is False:
            print("Failed to connect to Deepgram")
            return

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")
        # sleep(30)  # wait 30 seconds to see if there is any additional socket activity
        # print("Really done!")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return
    
def greetUser():
    hour = int(time.strftime("%H"))
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("The current time is " + time.strftime("%I:%M %p"))
    speak("How do you want me to assist you today?")
    
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
            
            save_response_as_audio("Song not found in the music library")
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
                    save_response_as_audio(f"{i}. {headline}")
            else:
                save_response_as_audio("Failed to fetch data from the API")
    else: 
        response_ai = processAI(command)
        save_response_as_audio(response_ai) 
        

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
                        save_response_as_audio(completion.choices[0].message.content)
                         
                        # return completion.choices[0].message.content


if __name__=='__main__':
    
    # speak_asave_response_as_audio("Initializing Dexter...") # use cached audio
    # play_audio("initializing_audio.mp3")
    print("Initializing Dexter...")
    # greetUser()
    try: 
        # while True:
        process_input()
        print("Done")
    except Exception as e:
        print("Error while Parsing", e)
