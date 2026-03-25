import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pywhatkit
import wikipedia
from openai import OpenAI

# 🔑 Add your API key here
client = OpenAI(api_key="YOUR_API_KEY")

# Voice engine
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print("You:", command)
            return command
        except:
            return ""

# 🤖 AI Chat function
def ai_chat(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 🚀 Start Assistant
speak("Hello, I am your smart assistant")

while True:
    command = listen()

    # 🕒 Time
    if "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"Time is {time}")

    # 🌐 Google
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # ▶️ YouTube
    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    # 🎵 Play Songs
    elif "play" in command:
        song = command.replace("play", "")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    # 💬 WhatsApp
    elif "whatsapp" in command:
        speak("Enter phone number with country code")
        number = input("Enter number: ")
        speak("What message should I send?")
        msg = listen()
        speak("Sending message")
        pywhatkit.sendwhatmsg_instantly(number, msg)

    # 📖 Wikipedia
    elif "who is" in command or "what is" in command:
        person = command.replace("who is", "").replace("what is", "")
        info = wikipedia.summary(person, 2)
        speak(info)

    # ➗ Calculator
    elif "calculate" in command:
        speak("Say expression like 5 plus 3")
        exp = listen()
        exp = exp.replace("plus", "+").replace("minus", "-")
        exp = exp.replace("into", "*").replace("by", "/")
        try:
            result = eval(exp)
            speak(f"Answer is {result}")
        except:
            speak("Sorry, I can't calculate")

    # ❌ Exit
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        break

    # 🤖 AI fallback (MOST IMPORTANT 🔥)
    elif command != "":
        reply = ai_chat(command)
        speak(reply)