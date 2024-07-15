import speech_recognition as sr
import webbrowser
import pyttsx3
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init() #starts pyttxs3

def speak(text):
    print("Initializing Jarvis")
    engine.say(text)
    engine.runAndWait()


if __name__=='__main__':
    
    speak("Initializing Jarvis...")
    while True:
        # trigger word "Jarvis"
        # obtain audio from the microphone
            
        print("recongnizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source,timeout=2, phrase_time_limit=2) 
            
            command = recognizer.recognize_google(audio)  #voic-input --> command
            print(command)
            if(command.lower() == "jarvis"):
                pass 
        except Exception as e:
            print("Error {0}".format(e))
        
    
    