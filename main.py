# Our main file
import speech_recognition as sr

# Create a recognizer
r = sr.Recognizer()

# Open the microphone for capture
with sr.Microphone() as source:
    while True:
        audio = r.listen(source) #Sets the microphone as a soucer of audio
        
        print(r.recognize_google(audio, language='pt'))