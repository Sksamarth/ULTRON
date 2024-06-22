# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3 
import replicate
import datetime
import os
import wikipedia
import pywhatkit as kit
import webbrowser
import time
from ecapture import ecapture as ec

# Initialize the recognizer 
r = sr.Recognizer() 
 
# Function to convert text to
# speech
def speak(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voices',voices[1].id)
    engine.say(command) 
    engine.runAndWait()
     
# Loop infinitely for user to
# speak
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning Sir !\nIm Ultron \nHow can I Help you")
        speak("Good Morning Sir !\nIm Ultron \nHow can I Help you")
  
    elif hour >= 12 and hour < 17:
        print("Good Afternoon Sir !\nIm Ultron \nHow can I Help you")
        speak("Good Afternoon Sir !\nIm Ultron \nHow can I Help you")   
  
    else:
        print("Good Evening Sir !\nIm Ultron \nHow can I Help you")
        speak("Good Evening Sir !\nIm Ultron \nHow can I Help you")  

def takeCommand():    
    # Exception handling to handle
    # exceptions at the runtime 
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.5)
            print("\nlistening...")
            #listens for the user's input 
            audio2 = r.listen(source2)
            # Using google to recognize audio
            print("\nRecognition...")
            querry = r.recognize_google(audio2)
            querry = querry.lower()
            print(querry)
            return querry
                
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
            
    except sr.UnknownValueError:
        print("unknown error occurred")

# The meta/llama-2-7b-chat model can stream output as it's running.
system_prompt="you are a AI assistant and your name is ULTRON and you gave a answer in one or two setences"
def llm(promt,):
    try: 
        for event in replicate.stream(
            "meta/llama-2-7b-chat",
            input={
                "debug": False,
                "top_p": 1,
                "prompt":promt,
                "temperature": 0.75,
                "min_new_tokens": -1,
                "max_new_tokens":50,
                "prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
                "repetition_penalty": 1
            },
        ):
            print(event, end=" "),speak(event)
    except ConnectionError as e:
        print("connect a internet".format(e))

def task():
    clear = lambda: os.system('cls')
     
    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    
    while True:
        try:
            query = takeCommand().lower()
        except AttributeError as e:
            print('speak again well please...')
            speak('speak again well please...')
            continue 
        # All the commands said by user will be 
        # stored here in 'query' and will be
        # converted to lower case for easily 
        # recognition of command
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation error (when the search term has multiple possible meanings)
                print(f"There are multiple meanings for '{query}'. Please be more specific.")
                speak(f"There are multiple meanings for '{query}'. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                # Handle page not found error (when the search term does not match any Wikipedia page)
                print(f"'{query}' does not match any Wikipedia page. Please try again.")
                speak(f"'{query}' does not match any Wikipedia page. Please try again.")
 
        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")
 
        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")
 
        # elif 'open stackoverflow' in query:
        #     speak("Here you go to Stack Over flow.Ha ppy coding")
        #     webbrowser.open("stackoverflow.com")   
 
        elif 'play music' in query or "play song" in query:
            speak("Here you go with music")
            # music_dir = "G:\\Song"
            music_dir = "C:\\Users\\sksam\\OneDrive\\Desktop\\pro\\songs"
            songs = os.listdir(music_dir)
            print(songs)    
            random = os.startfile(os.path.join(music_dir, songs[1]))
 
        elif ('what is time now') in query or ('what is the time now') in query or ('time') in query:
            strTime = time.ctime()
            
            print(strTime)   
            speak(f"Sir, the time is {strTime}")

 
        elif 'open vs code' in query:
            codePath = r"C:\\Users\\sksam\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
 
        elif ('ok exit') in query or ("thank you") in query or ("ok bye") in query or ("thank") in query:
            print("thank you for using our Assistant.. ")
            speak("thank you for using our Assistant.. ")
            break
        
    
        elif 'search' in query:
            s = query.replace('search', '')
            kit.search(s)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "hello" in query or "hi" in query or "what is your name" in query or "who are you" in query or "your name" in query:
            print("Hello Im Ultron")
            speak("Hello Im Ultron")
        elif 'code' in query or "code operation" in query or "code edit" in query:
            print('____________________\n|enter a sourcecode|\n_____________________')
            speak('you enter a source code-->')
            sourcecode = input('-->')
            speak("what you will do..")
            try:
                code = takeCommand()
                operation = str(f"{sourcecode}  {code} ")
                llm(operation)
            except AssertionError as e:
                print("error")
        else:
            llm(query)

if __name__ == '__main__':
    task()
