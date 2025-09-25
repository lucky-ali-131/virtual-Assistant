import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit as kit
import os
import tkinter as tk
import threading
import webbrowser

# For give voice output
engine = pyttsx3.init()

# Speed and volume of ai voice
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)
# Function for what jarvis say
def speak(text):
    engine.say(text)
    engine.runAndWait()

# User voice command input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # To ignore background noice
        audio = recognizer.listen(source)
    
    try:
        print("Processing...")
        command = recognizer.recognize_google(audio, language='en-in') # Input voice 
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.") # if ai not found command in code
        command = None
    except sr.RequestError:
        print("Sorry, the service is down.") # If data is turned off
        command = None
    
    return command.lower() if command else ""

# For whish (Good morning, etc)
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening sir !")
    speak("I am Jarvis, your personal assistant. How can I help you today?")  # After greeting command

# Connect to wikipedia
def search_wikipedia(query):
    speak(f"Searching Wikipedia for {query}...")

# Function to play any video on youtube
def play_music(song):
    speak(f"Playing {song}")
    kit.playonyt(song)

# Function to open doenloaded applications
def open_application(app_name):
    if 'chrome' in app_name:
        speak("Opening Google Chrome.")
        os.system("start chrome")
    elif 'firefox' in app_name:
        speak("Opening Mozilla Firefox.")
        os.system("start firefox")
    elif 'notepad' in app_name:
        speak("Opening Notepad.")
        os.system("start notepad")
    elif 'calculator' in app_name:
        speak("Opening Calculator.")
        os.system("start calc")
    else:
        speak(f"Sorry, I cannot open {app_name}.")

# Function to open websites by name
def open_website(command):

    websites = {
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "education": "https://www.okxxx2.pro"
    }
    
    # Extract website name from the command
    website_name = command.replace("go to", "").strip()

    if website_name in websites:
        speak(f"Opening {website_name}...")
        webbrowser.open(websites[website_name])
    else:
        if website_name.startswith("http://") or website_name.startswith("https://"):
            speak(f"Opening {website_name}...")
            webbrowser.open(website_name)
        else:
            speak(f"Sorry, I couldn't recognize the website {website_name}.")

# Function to handle custom questions and answers


def handle_custom_questions(command):
    custom_dict = {
        "what is your name": "My name is Jarvis.",
        "who make you": "Md Ali",
        "is ai is dangerous for humans": "no. artificial intelligence, is like a super smart robot that can learn and think. it's really powerfull and can do anything or amazing thing but it can also be a bit scary. scary degnified that jobloss privacy autonomus wepon missinformation. but don't worry so much smart people are working hard to make sure ai , use safely and ethically. and ai distroy anytime because creater of ai is human",
        "which is the best polytechnic college": "Government polytechnic sitamarhi",
        "why mbbs is tough": "the full form of mbbs is bachelor of medicine and bachelor of surgery. pursuing an mbbs degree comes with its fair share of challenges.the academic rigor of the program is often the hurdle students encounter ",
        "what is difference between download and install": "Downloading: Downloading means transfering a file from a remote server to local device.this file could a program,document,a video,or anything else.    installing means setting up a program or application on your device, so that it can be used.these usally invole extacting file from the downloded file and copying them to specific location on your device storage."
    }
    if command in custom_dict:
        speak(custom_dict[command])
    else:
        speak("Sorry, I don't know the answer to that question.")

# Function to create a custom screen with black background and a blue ring
def create_custom_screen():
    window = tk.Tk()
    window.title("Jarvis Assistant")
    window.geometry("800x600")
    window.configure(bg="black")
    
    canvas = tk.Canvas(window, width=800, height=600, bg="black", bd=0, highlightthickness=0)
    canvas.pack()
    center_x = 400
    center_y = 300
    radius = 180

    # Draw a blue ring in the center of the screen
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                        outline="blue", width=18)
    canvas.create_text(center_x, center_y, text="JARVIS", font=("Helvetica", 16), fill="white")

    window.mainloop()

# Main function to run the assistant
def main():
    greet()
    gui_thread = threading.Thread(target=create_custom_screen)
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        command = listen()

        if 'over' in command or 'Goodbye' in command:
            speak("Goodbye! Have a nice day.")
            break
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}.")
        elif 'search' in command:
            query = command.replace("search", "").strip()
            if query:
                search_wikipedia(query)
        elif 'play' in command:
            song = command.replace("play", "").strip()
            play_music(song)
        elif 'open' in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
        elif 'go to' in command:
            open_website(command)
        elif 'who are you' in command or 'who is the best polytechnic college' or 'why mbbs is tough' or 'ham kaun hain' or 'what is difference between download and install' or 'is ai is dangerous for humans' in command:
            handle_custom_questions(command)
        #elif 'go to' in command:
           # open_website(command)
        else:
            speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
