# # Our main file
# import speech_recognition as sr

# # Create a recognizer
# r = sr.Recognizer()

# # Open the microphone for capture
# with sr.Microphone() as source:
#     while True:
#         audio = r.listen(source) #Sets the microphone as a soucer of audio
        
#         print(r.recognize_google(audio, language='pt'))

# IMPORTANDO O VOSK PARA RECONHECIMENTO DE VOZ
#!/usr/bin/env python3


#!/usr/bin/env python3
import vosk 
import pyaudio
import argparse
import os
import queue
import sounddevice as sd
import sys
import pyttsx3
import json
from core import SystemInfo
from nlu.classifier import classify

# Síntese de fala
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[22].id)

def speak(text): 
    engine.say(text) #motor
    engine.runAndWait()

# Reconhecimento de fala

# Reconhecimento de Voz
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',channels=1, callback=callback):
        print('#' * 80)
        print('Press Ctrl+C to stop the recording')
        print('#' * 80)

        rec = vosk.KaldiRecognizer(model, args.samplerate)
        # Loop do reconhecimento de fala
        while True:
            data = q.get()
            if dump_fn is not None:
                dump_fn.write(data)
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result = json.loads(result) 
                # converter para json para que
                #possamos acessar os seus membros
                # print(result) # result é um destinário

                if result is not None: # função para Mila falar
                    text = result['text']
                    
                    # Reconhecer Entidade do texto.
                    entity = classify(text)


                    if entity == 'time/getTime':
                        speak(core.SystemInfo.get_time())
                    
                    print('Text: {}  Entity: {}'.format(text, entity))

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))


# python3.8 main.py