"""
Intelligent Voice Assistant (Jarvis-like)

Features:
- Speech I/O (pyttsx3 + speech_recognition)
- Wikipedia search
- Web automation (basic selenium flows)
- Screenshot capture
- Camera capture & selfie
- File creation
- Simple email-sending stub (requires user credentials)
- System info (IP, battery)
- News fetch (newsapi stub)
- Internet speed launcher (Ookla CLI)
- Password generator
- Music playback (local and web)
- Many helpful utility functions and robust error handling

NOTES:
- Fill placeholders for email credentials, API keys, chromedriver paths, and file paths before running.
- Keep privacy in mind: do not paste real credentials in shared submissions.
"""

# ---------------------------
# Imports
# ---------------------------
import os
import sys
import time
import random
import socket
import datetime
import webbrowser
import smtplib
import threading
from pathlib import Path

# Third-party libraries (install via pip if missing)
import pyttsx3
import speech_recognition as sr
import wikipedia
import requests
from bs4 import BeautifulSoup
from PIL import ImageGrab
import psutil
import cv2
import pyautogui

# Selenium imports - optional and only used when chromedriver is available
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except Exception:
    webdriver = None

# Attempt to import a decorative logo (optional)
try:
    from art import logo
except Exception:
    logo = "=== JARVIS ===\n(Voice Assistant Project)\n"

# ---------------------------
# Global configuration/placeholders (update these)
# ---------------------------
EMAIL_ADDRESS = "[YOUR_EMAIL@gmail.com]"        # <-- fill before running email features
EMAIL_PASSWORD = "[YOUR_EMAIL_PASSWORD]"        # <-- fill before running email features
NEWSAPI_KEY = "[YOUR_NEWSAPI_KEY]"              # <-- optional, for show_news()
CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"  # <-- fill if you plan to use selenium
DEFAULT_MUSIC_DIR = Path.home() / "Music" / "English Songs"  # update if needed
SCREENSHOT_SAVE_DIR = Path.home() / "Pictures" / "Jarvis_Screenshots"
SELFIE_SAVE_DIR = Path.home() / "Pictures" / "Jarvis_Selfies"
SPEEDTEST_CLI_PATH = "C:\\Program Files\\Ookla Speedtest CLI\\speedtest.exe"  # optional

# Ensure directories exist
SCREENSHOT_SAVE_DIR.mkdir(parents=True, exist_ok=True)
SELFIE_SAVE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Voice engine setup
# ---------------------------
engine = pyttsx3.init('sapi5')  # on Windows, sapi5 is typical. On other OS, default engine will be used.
voices = engine.getProperty('voices')
# Some machines may not have many voices, fall back safely
try:
    # pick a voice index that exists; prefer 0 if 2 is out of range
    engine.setProperty('voice', voices[0].id if len(voices) < 3 else voices[2].id)
except Exception:
    # If voices access fails, ignore and continue with default
    pass
engine.setProperty('rate', 160)  # slightly slower, clearer speech

# ---------------------------
# Helper functions
# ---------------------------
def speak(text: str):
    """Speak the given text aloud and also print it for logging."""
    if text is None:
        return
    print("[Jarvis]:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # If speech engine fails, still print to console
        print("Speech engine error:", e)


def prispk(*values):
    """Print and speak combined values (keeps long output presentable)."""
    joined = " ".join(str(v) for v in values)
    print(joined)
    speak(joined)


def wish_me():
    """Greet the user according to the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. Please tell me how may I help you, Sir.")


def take_command(timeout: int = 6, phrase_time_limit: int = 8) -> str:
    """
    Listen from the microphone and return recognized text.
    Returns "None" (string) when recognition fails so caller can check easily.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            prispk("No voice detected. Please speak.")
            return "None"

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print("User said:", query)
        return query
    except sr.UnknownValueError:
        prispk("Sorry, I did not understand that. Could you repeat?")
    except sr.RequestError:
        prispk("Could not reach the recognition service. Check your internet connection.")
    except Exception as e:
        prispk("Recognition error:", str(e))
    return "None"


def take_screenshot(save_dir: Path = SCREENSHOT_SAVE_DIR) -> Path:
    """Take a screenshot and save it to a timestamped file. Returns file path."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = save_dir / f"Screenshot_{timestamp}.png"
    try:
        img = ImageGrab.grab()
        img.save(fname)
        prispk(f"Screenshot saved to {fname}")
        return fname
    except Exception as e:
        prispk("Failed to take screenshot:", e)
        return None


def get_ip_info():
    """Return host name and IP address."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        prispk(f"Computer name: {hostname}")
        prispk(f"Local IP address: {ip_address}")
        return hostname, ip_address
    except Exception as e:
        prispk("Failed to get IP info:", e)
        return None, None


def send_email(to_address: str, content: str, from_addr: str = EMAIL_ADDRESS, password: str = EMAIL_PASSWORD):
    """
    Send a basic plain-text email using Gmail's SMTP.
    Warning: For Gmail, you may need an App Password or enable less-secure apps (not recommended).
    This function will raise exceptions if credentials are not set correctly.
    """
    if "[YOUR" in from_addr or "[YOUR" in password:
        prispk("Email credentials not configured. Please update EMAIL_ADDRESS and EMAIL_PASSWORD.")
        return False
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_address, content)
        server.quit()
        prispk("Email sent successfully.")
        return True
    except Exception as e:
        prispk("Failed to send email:", e)
        return False


def make_directory(path: str, name: str):
    """
    Create a new directory at given path with the given name.
    Safely handles path separators and existing directories.
    """
    final_path = Path(path) / name
    try:
        final_path.mkdir(parents=True, exist_ok=False)
        prispk(f"Directory created at: {final_path}")
        return True
    except FileExistsError:
        prispk("Directory already exists:", final_path)
        return False
    except Exception as e:
        prispk("Failed creating directory:", e)
        return False


def show_battery_status():
    """Report battery percentage and plugged-in status (useful on laptops)."""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            prispk("Battery information not available on this device.")
            return
        plugged = battery.power_plugged
        percent = battery.percent
        plugged_text = "Plugged In" if plugged else "Not Plugged In"
        left_label = "Battery" if plugged else "Battery left"
        prispk(f"Sir, your {left_label} is {percent}% and it is {plugged_text}.")
    except Exception as e:
        prispk("Failed to retrieve battery status:", e)


# ---------------------------
# News (NewsAPI stub)
# ---------------------------
def show_news(api_key: str = NEWSAPI_KEY):
    """
    Fetch top headlines via NewsAPI.org (requires an API key).
    If no API key is provided, fallback to scraping a simple Google news search result (less reliable).
    """
    if api_key and not api_key.startswith("["):
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {"country": "us", "apiKey": api_key, "pageSize": 10}
            res = requests.get(url, params=params, timeout=8)
            data = res.json()
            articles = data.get("articles", [])
            prispk("Top headlines:")
            for idx, art in enumerate(articles, start=1):
                prispk(f"{idx}. {art.get('title')}")
            return
        except Exception as e:
            prispk("NewsAPI fetch failed:", e)

    # Fallback: simple Google news scraping (fragile)
    try:
        prispk("Fetching news (fallback)...")
        r = requests.get("https://www.google.com/search?q=latest+news&tbm=nws", timeout=8,
                         headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        headlines = [h.get_text() for h in soup.select("div.BNeawe.vvjwJb.AP7Wnd")[:7]]
        for i, h in enumerate(headlines, start=1):
            prispk(f"{i}. {h}")
    except Exception as e:
        prispk("Failed to fetch news:", e)


# ---------------------------
# Selenium-based web helper (optional)
# ---------------------------
class BrowserController:
    """
    Simple wrapper to handle a single Selenium browser instance.
    Instantiate only if selenium webdriver is available and chromedriver path is provided.
    """

    def __init__(self, chromedriver_path: str = CHROMEDRIVER_PATH):
        self.browser = None
        self.opened = False
        self.chromedriver_path = chromedriver_path

    def open_browser(self, url: str = "https://www.google.com"):
        if webdriver is None:
            prispk("Selenium is not available on this system.")
            return False
        try:
            if not Path(self.chromedriver_path).exists():
                prispk("Chromedriver not found at path:", self.chromedriver_path)
                return False
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            self.browser = webdriver.Chrome(self.chromedriver_path, options=options)
            self.browser.get(url)
            self.opened = True
            prispk("Browser opened.")
            return True
        except Exception as e:
            prispk("Failed to open browser:", e)
            return False

    def search_google(self, query: str):
        if not self.opened or self.browser is None:
            if not self.open_browser():
                return False
        try:
            search_box = self.browser.find_element("name", "q")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            prispk("Searched Google for:", query)
            return True
        except Exception as e:
            prispk("Browser search failed:", e)
            return False

    def close(self):
        try:
            if self.browser:
                self.browser.quit()
            self.opened = False
            prispk("Browser closed.")
        except Exception as e:
            prispk("Error closing browser:", e)


# Global browser controller instance (kept so commands can close it)
browser_ctrl = BrowserController()


# ---------------------------
# Camera & selfie helpers
# ---------------------------
def open_camera_and_capture(save_dir: Path = SELFIE_SAVE_DIR):
    """Open webcam, display stream, capture on space, quit on Esc."""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            prispk("Could not open the camera.")
            return

        count = 0
        rand_suffix = random.randint(1000, 9999)
        prispk("Camera opened. Press SPACE to take a photo, ESC to exit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                prispk("Failed to read frame from camera.")
                break
            cv2.imshow("Jarvis Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                prispk("Closing camera.")
                break
            if key == 32:  # Space
                prispk("Say cheeeese!")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                fname = save_dir / f"img_{timestamp}_{rand_suffix}_{count}.jpg"
                cv2.imwrite(str(fname), frame)
                prispk("Saved selfie to", fname)
                count += 1
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        prispk("Camera error:", e)


# ---------------------------
# Password generator
# ---------------------------
def generate_password(length: int = 12, count: int = 5) -> list:
    """Generate `count` passwords of `length` characters each."""
    import string
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()_+{}[];<>?,./"
    passwords = []
    for _ in range(count):
        pw = "".join(random.choice(chars) for __ in range(length))
        passwords.append(pw)
    return passwords


# ---------------------------
# Main interactive loop
# ---------------------------
def main_loop():
    speak(logo)
    wish_me()

    while True:
        query = take_command().lower()

        if query == "none" or not query.strip():
            # If recognition failed or empty input, continue listening
            continue

        # ---------- Knowledge & web ----------
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            q = query.replace("wikipedia", "").strip()
            if not q:
                prispk("Please tell me what to search on Wikipedia.")
                continue
            try:
                summary = wikipedia.summary(q, sentences=4)
                prispk("According to Wikipedia:", summary)
            except Exception as e:
                prispk("Wikipedia search failed:", e)

        elif 'meaning' in query:
            prispk("Searching meaning on web...")
            q = query.replace("meaning", "").strip()
            if not q:
                prispk("Please tell me the word whose meaning you want.")
                continue
            # Try simple google search open in browser (fallback)
            webbrowser.open(f"https://www.google.com/search?q=define+{q}")
            prispk("Opened browser for the meaning.")

        elif ('wake up' in query) or ('wakeup' in query) or ('activate' in query):
            activation = ['Jarvis activated, Sir!', 'At your service!', 'Jarvis online.']
            prispk(random.choice(activation))

        # ---------- Browser automation ----------
        elif 'open google' in query:
            prispk("Opening Google.")
            speak("Sir, what should I search on Google?")
            q = take_command()
            if q and q != "None":
                webbrowser.open(f"https://www.google.com/search?q={q}")
            else:
                webbrowser.open("https://www.google.com")

        elif 'meaning' in query and ('google' in query or 'search' in query):
            # old logic replaced by simpler search
            pass

        elif 'open browser' in query or 'open chrome' in query:
            prispk("Opening Chrome.")
            try:
                # Try to open default chrome path if present
                if Path(CHROMEDRIVER_PATH).exists() and webdriver is not None:
                    browser_ctrl.open_browser()
                else:
                    # Fall back to launching system default browser
                    webbrowser.open("https://www.google.com")
            except Exception as e:
                prispk("Failed to open browser:", e)

        elif 'close browser' in query:
            browser_ctrl.close()

        # ---------- Utility ----------
        elif 'toss' in query or 'coin' in query:
            toss = random.choice(["Heads", "Tails"])
            prispk(toss)
            speak(toss)

        elif 'screenshot' in query or 'screen shot' in query:
            take_screenshot()

        elif 'weather' in query or 'temperature' in query:
            # quick fallback: open google weather for user's location
            prispk("Opening weather report in browser.")
            webbrowser.open("https://www.google.com/search?q=weather")
            # advanced: implement a weather API call if needed

        elif 'sign in' in query and 'facebook' in query:
            prispk("Attempting to open Facebook sign-in page.")
            if webdriver is None:
                prispk("Selenium not available. Opening Facebook in the browser instead.")
                webbrowser.open("https://www.facebook.com")
            else:
                if Path(CHROMEDRIVER_PATH).exists():
                    if browser_ctrl.open_browser("https://www.facebook.com"):
                        prispk("Browser open to Facebook. You may sign in manually.")
                else:
                    prispk("Please set CHROMEDRIVER_PATH to use automated sign-in.")

        elif 'what can you do' in query:
            prispk("I can search the web, play music, take screenshots, capture selfies, send emails (with credentials), fetch news, create folders, and more.")

        # ---------- Greetings ----------
        elif any(word in query for word in ['hello', 'hi', 'hey']):
            speak(random.choice(["Hello there!", "Hi!", "Hello! I am Jarvis."]))

        elif 'how are you' in query:
            speak("I am always ready and running, Sir. How are you?")

        elif 'who are you' in query:
            speak("I am Jarvis, an intelligent voice assistant created in Python.")

        elif 'thank you' in query:
            speak("You are very welcome.")

        # ---------- Open websites ----------
        elif 'open youtube' in query:
            speak("Opening YouTube. What should I search?")
            q = take_command()
            webbrowser.open(f'https://www.youtube.com/results?search_query={q}')

        elif 'open whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com")
            prispk("WhatsApp Web opened in browser.")

        elif 'open facebook' in query:
            webbrowser.open("https://www.facebook.com")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")

        elif 'open twitter' in query:
            webbrowser.open("https://www.twitter.com")

        # ---------- System control ----------
        elif 'play music' in query or 'music' in query:
            try:
                if DEFAULT_MUSIC_DIR.exists():
                    songs = list(DEFAULT_MUSIC_DIR.glob("*"))
                    if songs:
                        prispk("Playing a track from your music directory.")
                        os.startfile(songs[0])
                    else:
                        prispk("No songs found in configured music directory.")
                else:
                    prispk("Music directory not found. Opening YouTube music.")
                    webbrowser.open("https://music.youtube.com")
            except Exception as e:
                prispk("Failed to play music:", e)

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open code' in query:
            # Example: VS Code path (user-specific)
            code_path = r"C:\Users\idhant\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            if Path(code_path).exists():
                os.startfile(code_path)
            else:
                prispk("VS Code path not found, please update the configuration.")

        elif 'open zoom' in query:
            zoom_path = r"C:\Users\idhant\AppData\Roaming\Zoom\bin\Zoom.exe"
            if Path(zoom_path).exists():
                os.startfile(zoom_path)
            else:
                prispk("Zoom path not found. Open Zoom manually or update the path variable.")

        elif 'battery' in query:
            show_battery_status()

        # ---------- Email examples ----------
        elif 'email to' in query or ('send email' in query and 'to' in query):
            # Basic flow: ask for content and recipient
            prispk("Who is the recipient? Please say the recipient's email or 'myself' to send to your configured address.")
            recipient = take_command()
            if recipient and recipient != "None":
                prispk("What should I say?")
                content = take_command()
                if recipient.lower() in ['myself', 'me']:
                    to = EMAIL_ADDRESS
                else:
                    # If user said an email, we assume it's spelled correctly; in real project you may parse contact names
                    to = recipient
                if content and content != "None":
                    send_email(to, content)
                else:
                    prispk("No email content provided.")
            else:
                prispk("No recipient provided.")

        # ---------- File and folder ----------
        elif 'make' in query and 'file' in query or ('create' in query and 'folder' in query):
            speak("Please tell me the path where you want the directory created, or say 'desktop'.")
            p = take_command()
            if 'desktop' in p:
                base = str(Path.home() / "Desktop")
            elif 'home' in p:
                base = str(Path.home())
            else:
                prispk("Please type (or paste) the path into the console now:")
                base = input("Path: ").strip() or str(Path.home())
            speak("Please tell me the name of the directory to create.")
            name = take_command()
            if name and name != "None":
                make_directory(base, name)
            else:
                prispk("No name provided; aborting folder creation.")

        # ---------- Camera ----------
        elif 'camera' in query or 'selfie' in query or 'take picture' in query:
            open_camera_and_capture()

        # ---------- Internet / speed ----------
        elif 'internet' in query and 'speed' in query:
            if Path(SPEEDTEST_CLI_PATH).exists():
                prispk("Launching speedtest CLI.")
                os.startfile(SPEEDTEST_CLI_PATH)
            else:
                prispk("Speedtest CLI not configured. You can install Ookla CLI and update SPEEDTEST_CLI_PATH.")

        # ---------- Downloads & automation ----------
        elif 'download' in query and 'youtube' in query:
            prispk("Please paste the Youtube link into the console now:")
            link = input("Video link: ").strip()
            if link:
                webbrowser.open(link)
                prispk("Opened video link. Use a downloader plugin or site to save the video.")
            else:
                prispk("No link provided.")

        elif 'news' in query:
            show_news()

        # ---------- Password generator ----------
        elif 'generate' in query and 'password' in query:
            prispk("Enter desired password length (number) in the console:")
            try:
                length = int(input("Password length: ").strip() or "12")
            except ValueError:
                length = 12
            pwds = generate_password(length=length, count=5)
            prispk("Here are some password suggestions:")
            for idx, p in enumerate(pwds, 1):
                prispk(f"{idx}. {p}")

        # ---------- Misc small features ----------
        elif 'quiz' in query:
            speak('Tell me, who is the smartest person in the world?')
            answer = take_command()
            if 'jarvis' in answer.lower():
                speak('Right answer!')
            else:
                speak('Wrong answer. Try again.')

        elif 'ip' in query:
            get_ip_info()

        elif 'stop' in query or 'goodbye' in query or 'exit' in query:
            speak("Goodbye Sir. Have a great day!")
            sys.exit(0)

        else:
            # Fallback: open a google search for the query
            prispk("I did not find a matching command. Searching the web for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        prispk("Program interrupted by user. Exiting gracefully.")
    except Exception as e:
        prispk("An unexpected error occurred:", e)

