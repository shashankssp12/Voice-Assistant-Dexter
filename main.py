import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import time
import requests #library to fetch the api and access the methods in it


# --------------TODO: Make different file for all the sensitive info.
news_api = "bd7d86a2d1e24e65b1c01c7b961b6253"
url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}'
# --------------



recognizer = sr.Recognizer() # Creating an instance of the Recognizer class from the speech rec library
# `engine = pyttsx3.init()` initializes the pyttsx3 engine, which is a text-to-speech conversion
# library in Python. This line of code creates an instance of the pyttsx3 engine that can be used to
# convert text into spoken words.
engine = pyttsx3.init() #starts pyttxs3

def speak(text):
    print("Initializing Dexter..")
    engine.say(text)
    engine.runAndWait()
def processCommand(command):
    print(command)
    if "google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open linkedin" in command.lower():
            webbrowser.open("https://linkedin.com")
    elif "coding ninjas" in command.lower():
            webbrowser.open("https://codingninjas.com")
    elif "open github" in command.lower():
            webbrowser.open("https://github.com")
    elif "open youtube" in command.lower():
            webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
            song = command.lower().split(" ")[1] #TODO: See how two letter songs can be searched for.
            link = musicLibrary.music[song]
            webbrowser.open(link)
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
        # let openAI handle the code 
        pass
            
if __name__=='__main__':
    
    speak("Initializing Dexter...")
    while True:
        # trigger word "dexter"
        # obtain audio from the microphone
            
        print("recongnizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                # print("Say: Hi Dexter")
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1) 
            trigger_word = recognizer.recognize_google(audio)  #voic-input --> command
            print(trigger_word)
            if "dexter" in trigger_word.lower():
                speak("Sir!")
                with sr.Microphone() as source:
                    print("Say the command on...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)  #voice-input --> command
                    processCommand(command)
        except Exception as e:
            print("Parsing..{0}".format(e))
        
    