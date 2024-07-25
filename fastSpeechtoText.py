import speech_recognition as sr

# fast program to do speech to text conversion using google speech recognition api
# Initialize the recognizer
r = sr.Recognizer()

# Use the microphone as the source for input
with sr.Microphone() as source:
    print("Speak something...")
    audio = r.listen(source)

try:
    # Use Google Speech Recognition to convert speech to text
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand your speech")
except sr.RequestError as e:
    print("Sorry, I could not request results from Google Speech Recognition service; {0}".format(e))