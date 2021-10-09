import datetime
import os
import random
import sys
import time
import webbrowser
import cv2
import pyautogui
import pyttsx3
import speech_recognition
import wikipedia
import pywhatkit
import pyjokes
from PIL import ImageGrab
from requests import get

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


def greetingTime():
    gt = time.localtime().tm_hour
    if 4 <= gt < 12:
        speak("Good Morning Sir!")
    elif 12 <= gt < 16:
        speak("Good Afternoon Sir!")
    elif 16 <= gt < 20:
        speak("Good Evening Sir!")
    elif 20 <= gt <= 24:
        speak("Glad to see you again!")
    else:
        speak("Glad to see you again!")


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 5
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User's command : {query}")

    except Exception as e:
        speak("Sorry, I can't recognize")
        speak("Say again please")
        takeCommand()
        return "none"
    return query


if __name__ == "__main__":
    greetingTime()
    run = True
    while run == True:
        query = takeCommand().lower()
        # logics of query

        if "ip address" in query or "ip" in query:
            ip = get("https://api.ipify.org").text
            speak(f"Your IP address is {ip}")

        if "send message" in query or "whatsapp" in query:
            speak("Whom do you want to send message??")
            mobnum = input(speak("Enter here: "))
            num = mobnum
            speak("What messege do you want to send??")
            mes = takeCommand().lower()
            time.sleep(5)
            speak("What time: ")
            hr = int(input("Hour: "))
            mins = int(input("Min: "))
            pywhatkit.sendwhatmsg(f"+91 {num}", mes, hr, mins, 10,True,20)
            if 1:
                pyautogui.click(x=1865, y=964,clicks=1)
            if True:
                speak("Messege sent!")

        if "screenshot" in query or "screen image" in query or "screen grab" in query or "grab screen" in query or "snip" in query:
            screenshot=ImageGrab.grab()
            screenshot.show()
            speak("Screenshot taken")

        if "wikipedia" in query or "wiki" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            speak(results)

        if "play music" in query or "music" in query:
            music_dir = "Music"
            songs = os.listdir(music_dir)
            rs = random.choice(songs)
            os.startfile(os.path.join(music_dir, rs))

        if "open edge" in query or "open bing" in query:
            speak("Opening MS Edge")
            speak("What should I search in MS Edge?")
            cm = query
            speak(f'Searching {cm} in MS Edge')
            webbrowser.open(f'https://www.bing.com/search?q={cm}')

        if "close edge" in query or "close bing" in query:
            speak("Closing MS Edge")
            os.system(
                "taskkill /f /im C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")

        if "open control panel" in query or "open cp" in query:
            speak("Opening Control Panel")
            cp = r"C:\WINDOWS\System32\control.exe"
            os.startfile(cp)

        if "close control panel" in query or "close cp" in query:
            speak("Closing Control Panel")
            os.system("taskkill /f /im C:\\WINDOWS\\System32\\control.exe")

        if "open powerpoint" in query or "open presentation" in query or "open ppt" in query:
            speak("Opening MS Access")
            ppt = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.exe"
            os.startfile(ppt)

        if "close powerpoint" in query or "close presentation" in query or "close ppt" in query:
            speak("Closing Access")
            os.system("taskkill /f /im POWERPNT.exe")

        if "open word" in query or "open ms word" in query or "open docs" in query:
            speak("Opening MS Word")
            word = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.exe"
            os.startfile(word)

        if "close word" in query or "close ms word" in query or "close docs" in query:
            speak("Closing Word")
            os.system("taskkill /f /im WINWORD.exe")

        if "open ms access" in query or "open access" in query or "open ms db" in query:
            speak("Opening MS Access")
            msaccess = r"C:\Program Files\Microsoft Office\root\Office16\MSACCESS.exe"
            os.startfile(msaccess)

        if "close ms access" in query or "close access" in query or "close ms db" in query:
            speak("Closing Access")
            os.system("taskkill /f /im MSACCESS.exe")


        if "open zoom" in query:
            speak("Opening Zoom")
            zpath=r"C:\Users\Amit Rathod\AppData\Roaming\Zoom\bin\Zoom.exe"
            os.startfile(zpath)
        if "close zoom" in query:
            speak("Closing Zoom")
            os.system("taskkill /f /im Zoom.exe")

        if "open camera" in query or "camera" in query or "take photo" in query or "take picture" in query:
            cap = cv2.VideoCapture(0)
            count = 0
            b = random.randint(1, 10000)
            while True:
                ret, img = cap.read()
                cv2.imshow("Camera", img)
                if not ret:
                    break
                k = cv2.waitKey(50)
                if k % 256 == 27:
                    print("Closing Camera")
                    break

                if k % 256 == 32:
                    speak("Say Cheeeeeese..")
                    time.sleep(1)
                    speak("Picture saved")
                    file = r'Pictures\img' + str(count) + str(b) + '.jpeg'
                    cv2.imwrite(file, img)
                    count += 1
            cap.release()
            cv2.destroyAllWindows()

        if "open youtube" in query:
            speak("Opening YouTube")
            speak("What should I search in YouTube?")
            cm = query
            speak(f'Searching {cm} in YouTube')
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={cm}")

        if "open google" in query:
            speak("Opening Google")
            speak("What should i search in Google ?")
            cm = takeCommand().lower()
            speak(f'Searching {cm} in Google')
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        if "close google" in query:
            speak("Closing Google")
            os.system("taskkill /f /im chrome.exe")

        if "open command prompt" in query or "open cmd" in query or "open prompt" in query:
            speak("Opening command prompt")
            os.system("start cmd")

        if "close command prompt" in query or "close cmd" in query or "close prompt" in query:
            speak("Closing command prompt")
            os.system("taskkill /f /im cmd.exe")

        if "open pycharm" in query:
            speak("Opening pycharm")
            pycharmpath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2021.2.2\\bin\\pycharm64.exe"
            os.startfile(pycharmpath)

        if "close pycharm" in query:
            speak("Closing pycharm")
            os.system("taskkill /f /im pycharm64.exe")

        if "open eclipse" in query:
            speak("Opening Eclipse")
            eclpath = r"C:\Users\Amit Rathod\eclipse\java-2021-03\eclipse\eclipse.exe"
            os.startfile(eclpath)

        if "close eclipse" in query:
            speak("Closing Eclipse")
            os.system("taskkill /f /im eclipse.exe")

        if "open Code" in query or "open vsc" in query or "open studio" in query:
            speak("Opening VS Code")
            VSC = "C:\\Users\\Amit Rathod\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(VSC)

        if "close Code" in query or "close vsc" in query or "close studio" in query:
            speak("Closing VS Code")
            os.system("taskkill /f /im Code.exe")

        if "how are you" in query or "what about you" in query:
            speak("I'm alright!")
            speak("What about You??")
            takeCommand().lower()
            if True:
                speak("Glad to see you safe!")

        if "hi" in query or "hello" in query:
            speak("Hello! Sir")


        if "open notepad" in query:
            speak("Opening Notepad")
            npPath = r"C:\WINDOWS\system32\notepad.exe"
            os.startfile(npPath)

        if "close notepad" in query:
            speak("Closing notepad")
            os.system("taskkill /f /im notepad.exe")

        if "time" in query or "current time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Current time is {time}")

        if "alarm" in query or "set alarm" in query:
            ahr=int(datetime.datetime.now().hour)
            amin = str(datetime.datetime.now().min)

            hrs=int(input("Enter hour:"))
            mins=int(input("Enter Minutes:"))
            while ahr==hrs and amin==mins:
                while True:
                    music_dir="Music"
                    songs=os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir,songs[0]))

        if "joke" in query or "jokes" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        #
        # if "shutdown" in query:
        #     os.system("shutdown /s /t 5")
        #
        # if "restart" in query:
        #     os.system("shutdown /r /t 5")
        #
        # if "sleep system" in query:
        #     os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        if "play store" in query:
            speak("Opening Play Store")
            speak("What App should I search in Play Store ?")
            cm = takeCommand().lower()
            speak(f'Searching {cm} in Play Store')
            webbrowser.open(f"https://play.google.com/store/search?q={cm}&c=apps")

        if "switch tab" in query or "switch tabs" in query or "change tabs" in query or "change tab" in query:
            speak("How many tabs do you want to switch")
            tab=0
            cm=takeCommand().lower()
            if "one" in cm or "1" in cm:
                tab=1
            if "two" in cm or "to" in cm or "2" in cm or "tu" in cm:
                tab=2
            if "three" in cm or "3" in cm or "free" in cm or "tree" in cm or "tre" in cm:
                tab=3
            if "four" in cm or "for" in cm or "4" in cm:
                tab=4
            if "five" in cm or "5" in cm:
                tab=5

            while tab>=0:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                tab =tab-1
            pyautogui.keyUp("alt")



        if "wait" in query:
            speak("For how long??")
            t = int(input(speak("Seconds: ")))
            time.sleep(t)

        #
        # if "news" in query:
        #     speak("Fetching latest headline...... Please wait!")
        #     news()

        if "thankyou" in query or "thank you" in query or "no thanks" in query:
            speak("You're Welcome!")
            run = False
            sys.exit()

        if "deactivate" in query:
            speak("Deactivated!")
            run = False
            sys.exit()

        if "good night" in query:
            speak("To you too....")
            run=False
            sys.exit()

        speak("Anything else??")
