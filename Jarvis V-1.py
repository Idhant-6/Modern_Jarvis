import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser   
import os
import smtplib
import time
import random
from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageGrab    # pip install pillow
import requests     # pip install requests
from bs4 import BeautifulSoup       # pip install bs4


# ALL LISTS
hello = ['Hi There', 'Hi', 'Hello', 'Hello! I am Jarvis!']
activation = ['Jarvis Activated Sir!', 'Jarvis Activated Succesfully Sir!', 'Anytime Sir!', 'Ok sir!', 'Yes sir!']

# Necessary Lines to make Machine Speak! DO NOT CHANGE UNTIL NECESSARY!
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[2].id)


def speak(audio):
    """Is Used to Make Machine Speak Anything You Want! Cool No!"""
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """Is Used To Wish the User By Speaking Good Morning, Afternoon and Evening On what the time is."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis. Please tell me how may I help you Sir")


def prispk(value):
    """Used to Both Speak And Print Commands at the Same Time!"""
    print(value)
    speak(value)


def takeScreenshot():
    """Is Used to Take Screenshot! and then opens the picture to Show What is taken!"""
    image = ImageGrab.grab()
    image.show()
    prints("Screenshot Taken Sir!")


def takeCommand():
    """Is Used to take microphone input from the user and return string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("What do You Mean Sir?")
        return "None"
    return query


def sendEmail(to, content):
    """Is Used to Send Email To Anyone Using Gmail Server!"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('[YOUR GMAIL EMAIL HERE]', '[YOUR PASSWORD HERE]')
    server.sendmail('YOUR EMAIL HERE AGAIN', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            prispk(results)

        elif 'draw' in query and 'dotted' in query or 'hirst' in query:
            speak("I hope that I could draw that... But I don't have that function.. Please Try Again after next Update.")

        elif 'wake up' in query or 'wakeup' in query:
            prints(random.choice(activation))

        elif 'what is' in query:
            time.sleep(1.5)
            speak('I am Searching For This in Google Sir...')
            query = query.replace("what is", "What is")
            browser = webdriver.Chrome('chromedriver.exe')
            browser.maximize_window()
            window_open = True
            browser.get('https://www.google.com')
            search = browser.find_element_by_name('q')
            search.send_keys(query)
            search.send_keys(Keys.ENTER)

        elif 'meaning' in query:
            time.sleep(1.5)
            speak('I am Searching For This in Google Sir...')
            query = query.replace("meaning", "What is the Meaning of")
            browser = webdriver.Chrome('desktop\\chromedriver.exe')
            browser.maximize_window()
            window_open = True
            browser.get('https://www.google.com')
            search = browser.find_element_by_name('q')
            search.send_keys(query)
            search.send_keys(Keys.ENTER)

        elif 'close' in query:
            if window_open:
                print("Closing The Window")
                browser.close()
            elif not window_open:
                prints("No Window is open sir!")
            else:
                speak("I'm Having Trouble Doing this sir!")

        elif 'toss' in query:
            toss = ["Heads", "Tails"]
            print(random.choice(toss))
            speak(random.choice(toss))

        elif 'screenshot' in query:
            takeScreenshot()

        elif 'weather' in query or 'temperature' in query:
            search = 'Temprature in California'
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div",class_= "BNeawe")
            speak(f"Current Weather in California is {temp}. Hope You're Good to Go Sir!")            

        elif 'what can you do' in query:
            speak("I can Do many Things.... Like... Open Google or any website and sign in to your facebook")


        elif 'hello' in query or 'hi' in query:
            speak(random.choice(hello))

        elif 'how are you' in query:
            speak("I am always fine, what about you?")

        elif 'am fine' in query:
            speak('Nice to hear that you are fine')

        elif 'who are you' in query:
            speak('I am Jarvis. A Cloud based AI Made by Programmer Lakshya')

        elif 'you are mad' in query:
            speak('I always want a feedback from my users, try saying "I have a feedback".')

        elif 'thank you' in query:
            speak('Your Very Very Welcome')

        elif 'where are you' in query:
            speak('I am here only')

        elif 'open youtube' in query:
            speak('opening youtube Sir')
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak('opening google sir')
            webbrowser.open("https://www.google.com")

        elif 'open scratch' in query:
            speak('opening scratch Sir')
            webbrowser.open("scratch.mit.edu")

        elif 'open whatsapp' in query:
            speak('opening whatsapp Sir')
            webbrowser.open("web.whatsapp.com")

        elif 'open facebook' in query:
            speak('opening facebook Sir')
            webbrowser.open("https://www.facebook.com")

        elif 'open instagram' in query:
            speak('opening instagram Sir')
            webbrowser.open("https://www.instagram.com")

        elif 'open twitter' in query:
            speak('opening twitter')
            webbrowser.open("twitter.com")

        elif 'ok' in query:
            speak('sure')

        elif 'your favorite color' in query:
            speak('My favorita color is white')

        elif 'your favorita car' in query:
            speak('My favorite car is the MG Gloster')

        elif 'your favorite bike' in query:
            speak('My favorite bike is Ducati Streetfighter V4')

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Admin\\Music\\English Songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'open firefox' in query:
            firefoxPath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
            os.startfile(firefoxPath)

        elif 'open chrome' in query:
            chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chromePath)

        elif 'open zoom' in query:
            zoomPath = "C:\\Users\\Admin\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
            os.startfile(zoomPath)

        elif 'open vlc media player' in query:
            vlcmediaplayerPath = "C:\\Program Files\\VLC\\vlc.exe"
            os.startfile(vlcmediaplayerPath)

        elif 'email to idhant' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "programmer.idhant@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent Sir!!")
            except Exception as e:
                print(e)
                speak("Sorry. But I am not able to send this email Sir!... You Can Still Try Again!")

        elif 'feedback' in query:
            try:
                speak("What do you want to say in feedback?")
                content = takeCommand()
                to = "programmer.idhant@gmail.com"
                sendEmail(to, content)
                speak("Your feedback has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry but I'm not able to send the feedback... Please Try Again...")
