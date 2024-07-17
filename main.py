import speech_recognition as sr
import webbrowser
import pyttsx3
import time

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
            
            
            
if __name__=='__main__':
    
    speak("Initializing Dexter...")
    while True:
        # trigger word "Jarvis"
        # obtain audio from the microphone
            
        print("recongnizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                # print("Say: Hi Eve")
                print("Listening...")
                audio = recognizer.listen(source) 

            trigger_word = recognizer.recognize_google(audio)  #voic-input --> command
            print(trigger_word)
            if "dexter" in trigger_word.lower():
                speak("Sir!")
                with sr.Microphone() as source:
                    print("Microphone on...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)  #voice-input --> command
                    processCommand(command)
        except Exception as e:
            print("Parsing..{0}".format(e))
        
    