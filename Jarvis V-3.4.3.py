import pyttsx3
from requests.api import put
import speech_recognition as sr 
import datetime
import wikipedia 
import sys
import webbrowser   
import os
import smtplib
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageGrab
import requests
from bs4 import BeautifulSoup
import psutil
import cv2
import speedtest
import pyautogui
from art.py import logo

# ALL LISTS
hello = ['Hi There', 'Hi', 'Hello', 'Hello! I am Jarvis!']
activation = ['Jarvis Activated Sir!', 'Jarvis Activated Successfully Sir!', 'Anytime Sir!', 'Ok sir!', 'Yes sir!']

# Necessary Lines to make Machine Speak! DO NOT CHANGE UNTIL NECESSARY!
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[2].id)


def speak(audio):
    """Is Used to Make Machine Speak Anything You Want..."""
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """Is Used To Wish the User By Speaking Good Morning, Afternoon and Evening On what the time is."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis. Please tell me how may I help you Sir")


def prispk(value):
    """Used to Both Speak And Print Commands at the Same Time."""
    print(value)
    speak(value)


def takeScreenshot():
    """Is Used to Take Screenshot! and then opens the picture to Show What is taken!"""
    image = ImageGrab.grab()
    image.show()
    image.save('[Path to Folder]')
    prispk("Screenshot Taken Sir!")

def getIP():
    """Is used to Grab Your Pc's IP Address"""
    import socket
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    prispk("Your Computer Name is: " + hostname)
    prispk("Your Computer's IP Address is: " + IPAddr)



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
        prispk("What do You Mean Sir?")
        return "None"
    return query


def sendEmail(to, content):
    """Is Used to Send Email To Anyone Using Gmail Server!"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('[YOUR EMAIL HERE]', '[PASSWORD HERE]')
    server.sendmail('[EMAIL HERE]', to, content)
    server.close()

def showBatteryOptions():
    """Is Used to Tell About Your Battery Level NOTE:- This Feature is only for laptops as they only run on Battries"""
    battery_detecting = psutil.sensors_battery()
    plugged = battery_detecting.power_plugged
    percent_battery = str(battery_detecting.percent)
    plugged = "Plugged In" if plugged else "Not Plugged In"
    if plugged == "Not Plugged In": 
        left_or_not = "Battery Left"
    else:
        left_or_not = "Battery"
    prispk(f"Sir Your {left_or_not} Is {percent_battery}% And {plugged}")


def make_file(path, name):
    final_path = f"{path}\{name}"
    os.mkdir(final_path)
    
def showNews():
    query_params = {
    "source": "bbc-news",
    "sortBy": "top",
    "apiKey": "d14ab386a383450fa57f83ac75cb2f01"
    }
    main_url = " https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    article = open_bbc_page["articles"]
    results = []
    
    for ar in article:
        results.append(ar["title"])
        
    for i in range(len(results)):
        prispk(i + 1, results[i])


if __name__ == "__main__":
    print(logo)
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
            prispk(random.choice(activation))


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
                prispk("No Window is open sir!")
            else:
                speak("I'm Having Trouble Doing this sir!")

        elif 'toss' in query:
            toss = ["Heads", "Tails"]
            print(random.choice(toss))
            speak(random.choice(toss))

        elif 'screenshot' in query:
            takeScreenshot()

        elif 'weather' in query or 'temperature' in query:
            # query = query.replace("weather" or 'temprature', "Weather of ")
            search = 'Temperature'
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("class",class_= "BNeawe")
            speak(f"Current {search}, is {temp}. Hope You're Good to Go Sir!")            

        elif 'sign in' in query:
            time.sleep(1.5)
            speak('Signing In To Facebook Sir')
            query = query.replace("sign in", "sign in")
            browser = webdriver.Chrome('desktop\\chromedriver.exe')
            browser.maximize_window()
            browser.get('https://www.facebook.com')
            fill = browser.find_element_by_id('email')
            fill.send_keys()
            # fill.send_keys(Keys.ENTER)
            password = browser.find_element_by_id("pass")
            password.send_keys("[your passoword]")
            fill.send_keys(Keys.ENTER)
            sign_in = True
            print("Sign in Succesful Sir!")
            speak("Sign in Succesful Sir!")

        # elif 'new tab' in query and window_open:
        #     new_tab = browser.find_element_by_tag("body")

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
            speak('I am here only...')

        elif 'open youtube' in query:
            speak('Opening Youtube Sir')
            speak("Sir What Should I search on Youtube??")
            query_youtube = takeCommand()
            webbrowser.open(f'https://www.youtube.com/results?search_query={query_youtube}')

        elif 'open google' in query:
            speak("Opening Google Sir")
            speak("Sir What Should I search on Google??")
            query_google = takeCommand()
            webbrowser.open(f"https://www.google.com/search?q={query_google}")
    
        elif 'open scratch' in query:
            speak('opening scratch Sir')
            webbrowser.open("https://scratch.mit.edu")

        elif 'open whatsapp' in query:
            speak('opening whatsapp Sir')
            webbrowser.open("https://web.whatsapp.com")

        elif 'open facebook' in query:
            speak('opening facebook Sir')
            webbrowser.open("https://www.facebook.com")

        elif 'open instagram' in query:
            speak('opening instagram Sir')
            webbrowser.open("https://www.instagram.com")

        elif 'open twitter' in query:
            speak('opening twitter')
            webbrowser.open("https://www.twitter.com")

        elif 'ok' in query:
            speak('sure')

        elif 'your favorite color' in query:
            speak('My favorita color is white')

        elif 'your favorita car' in query:
            speak('My favorite car is the MG Gloster')

        elif 'your favorite bike' in query:
            speak('My favorite bike is Ducati Streetfighter V4')

        elif 'quiz' in query:
            speak('Tell me, Who is the Smartest Person in the World.')
            user_answer = takeCommand()
            if 'Jarvis' in user_answer:
                speak('Right answer')
            else:
                speak('Wrong Answer')

        elif 'ip' in query:
            ip = getIP()
            prispk(ip)

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Admin\\Music\\English Songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\idhant\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'open chrome' in query:
            chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chromePath)

        elif 'open zoom' in query:
            zoomPath = "C:\\Users\\idhant\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
            os.startfile(zoomPath)

        elif 'battery' in query:
            showBatteryOptions()

        elif 'email to idhant' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "[YOUR FRIENDS EMAIL HERE]"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir, But I am not able to send this email")

        elif 'email' in query and 'mother' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "[EMAIL HERE]"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir, But I am not able to send this email")

        elif 'email' in query and 'father' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "[EMAIL HERE]"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Si, But I am not able to send this email")

        elif 'feedback' in query:
            try:
                speak("What do you want to say in feedback?")
                content = takeCommand()
                to = "popstar.idhant@outlook.com"
                sendEmail(to, content)
                speak("Your feedback has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir, but I'm not able to send the feedback... Please Try Again...")

        elif 'make' in query and 'file' in query:
            speak("Please Tell Me The Path that You Want to Make A File!\n")
            path = takeCommand()
            if 'desktop' in path:
                file_path = 'C:\\Users\\idhant\\OneDrive\\Desktop\\'
            elif 'input' in path:
                file_path = input("File Path Sir...\n")
            speak("Please Tell Me The Name Of The File You Want To Create!\n")
            file_name = takeCommand()
            make_file(file_path, file_name)
            prispk("File Made Successfully Sir!")  

        elif 'camera' in query:            
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

        elif 'internet' in query and 'speed' in query:
            # st = speedtest.Speedtest()
            # speak("Testing Your Internet Speed Sir!")
            # dl = st.download()
            # up = st.upload()
            # prispk(f'Download Speed is: {dl} Bits Per Second And Your upload speed is {up} Bits Per Second')
            speedtest_path = "C:\\Program Files\\Ookla Speedtest CLI\\speedtest.exe"
            speak("Checking Your Internet Speed Sir!")
            os.startfile(speedtest_path)

        elif 'music' in query:
            speak("Sir, Where Do You Want To Listen Music From??")
            user_choice = takeCommand()
            if "youtube" in user_choice:
                speak("Playing Music From Youtube Sir")
            elif "spotify" in user_choice:
                speak("Playing Music From Spotify Sir")
            elif "local" in user_choice:
                speak("Playing Music From The Local Dirctory Sir")

            
        elif 'download' in query and 'youtube' in query:
            speak("Sir, Please Give Me the Link Of the Video You Want To Download From Youtube")
            video_link = input("Your Video Link Here: ")
            webbrowser.open(video_link)
            time.sleep(5)
            pyautogui.moveTo(1138, 189, 1)
            pyautogui.click()
            pyautogui.moveTo(1284, 384, 1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.press('enter')
            speak("Sir, The Video Downloading is Started!")
            pyautogui.hotkey('win', 'e')
            
         elif 'news' in query:
            showNews()
             
         elif 'generate' in query and 'password' in query:
            if __name__ == "__main__":
                s1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','o','p','q','r','s','t','u','v','w','x','y','z']
                s2 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                s3 = ['1','2','3','4','5','6','7','8','9','0']
                s4 = ['!','@','#','$','%','^','&','*','(',')','_','+','{','}','|','[',']','"',';','<','>','?','/',',']
            
                passLen = int(input("Enter Your password lenght: "))
                s = []
                s.extend(s1)
                s.extend(s2)
                s.extend(s3)
                s.extend(s4)
                a =0
                print("Choose any one of the 5 passwords given below!")
                print("")
                while a<5:
                    random.shuffle(s)
                    print("\t","".join(s[0:passLen]))
                    a=a+1
            speak("Password created Sir!")

        elif 'selfie' in query or 'take picture':
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("Take selfie with python")
            img=0
            while True:
                ret, frame = cam.read()
                    
                if not ret:
                    print("Failed to grab frame") 
                    break
            
                cv2.imshow("Take selfie with python",frame)
                k = cv2.waitKey(1)
                if k%256 == 27:
                    print("Escape hit, closing the window")
                    break
                if k%256 == 32:
                    img_name = f"Selfie_{img}.jpg"
                    cv2.imwrite(img_name,frame)
                    print("Selfie taken!")
                    img+=1
            cam.release
            cv2.destroyAllWindows()
             
        elif 'stop' in query or 'goodbye' in query:
            speak("Good Byee Sir!, Hope You Have A Good Day!")
            sys.exit()

        

