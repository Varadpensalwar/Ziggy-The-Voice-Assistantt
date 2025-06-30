import os
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import pygame
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
import requests
import datetime
import threading
import shutil

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("ziggy.db")
cursor = con.cursor()

OPENWEATHER_API_KEY = "3a88be46249d14cc6ef20e261750c728"  # <-- Replace with your OpenWeatherMap API key
PORCUPINE_ACCESS_KEY = "deiFbpp9oD2JodPEZKsqdvYqSjMKlcWl/HgL/xIM82rNgQNrXiafnQ=="  # <-- Replace with your Picovoice Porcupine AccessKey

# Common app locations and names
COMMON_APPS = {
    'chrome': [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(os.getenv('USERNAME'))
    ],
    'brave': [
        r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        r'C:\Users\{}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe'.format(os.getenv('USERNAME'))
    ],
    'firefox': [
        r'C:\Program Files\Mozilla Firefox\firefox.exe',
        r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
    ],
    'edge': [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
    ],
    'notepad': [r'C:\Windows\System32\notepad.exe'],
    'calculator': [r'C:\Windows\System32\calc.exe'],
    'paint': [r'C:\Windows\System32\mspaint.exe'],
    'wordpad': [r'C:\Program Files\Windows NT\Accessories\wordpad.exe'],
    'explorer': [r'C:\Windows\explorer.exe'],
    'cmd': [r'C:\Windows\System32\cmd.exe'],
    'powershell': [r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe']
}

# Common websites
COMMON_WEBSITES = {
    'youtube': 'https://www.youtube.com',
    'google': 'https://www.google.com',
    'github': 'https://github.com',
    'facebook': 'https://www.facebook.com',
    'twitter': 'https://twitter.com',
    'instagram': 'https://www.instagram.com',
    'linkedin': 'https://www.linkedin.com',
    'gmail': 'https://mail.google.com',
    'outlook': 'https://outlook.live.com',
    'amazon': 'https://www.amazon.com',
    'netflix': 'https://www.netflix.com',
    'spotify': 'https://open.spotify.com',
    'stackoverflow': 'https://stackoverflow.com',
    'reddit': 'https://www.reddit.com',
    'wikipedia': 'https://www.wikipedia.org',
    'bing': 'https://www.bing.com',
    'yahoo': 'https://www.yahoo.com'
}

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_dir)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print(f"Error playing sound: {e}")

    
def find_app_path(app_name):
    """Find the path of an app by name."""
    app_name = app_name.lower()
    
    # Check database first
    cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
    results = cursor.fetchall()
    if results:
        return results[0][0]
    
    # Check common apps
    if app_name in COMMON_APPS:
        for path in COMMON_APPS[app_name]:
            if os.path.exists(path):
                return path
    
    # Try to find in PATH
    try:
        path = shutil.which(app_name)
        if path:
            return path
    except:
        pass
    
    # Try with .exe extension
    try:
        path = shutil.which(app_name + '.exe')
        if path:
            return path
    except:
        pass
    
    return None

def openCommand(query):
    """
    Enhanced app and website opening with smart detection.
    """
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()

    if not query:
        speak("Please specify what you want to open.")
        return

    try:
        # 1. Try to open as a local application
        app_path = find_app_path(query)
        if app_path:
            speak(f"Opening {query}")
            os.startfile(app_path)
            return

        # 2. Try to open as a known website
        if query in COMMON_WEBSITES:
            speak(f"Opening {query}")
            webbrowser.open(COMMON_WEBSITES[query])
            return
        
        # Check database for websites
        cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            webbrowser.open(results[0][0])
            return

        # 3. Try to open as a direct URL
        if re.match(r"^https?://", query):
            speak(f"Opening {query}")
            webbrowser.open(query)
            return

        # 4. Try to open as a domain (add https://)
        if '.' in query and ' ' not in query:
            url = f"https://{query}"
            speak(f"Opening {query}")
            webbrowser.open(url)
            return

        # 5. Fallback: perform a web search
        speak(f"I couldn't find '{query}' as an app or website. Searching the web for you.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        
    except Exception as e:
        speak(f"Something went wrong: {e}")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword(trigger_callback=None):
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("hotword detected")
                if trigger_callback:
                    trigger_callback()
                time.sleep(2)
    except Exception as e:
        print(f"Hotword error: {e}")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

def get_weather(city):
    """Fetch and speak the weather for a given city."""
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        speak("Weather feature is not set up. Please add your OpenWeatherMap API key in features.py.")
        return
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            speak(f"Sorry, I couldn't find weather for {city}.")
            return
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        city_name = data["name"]
        msg = f"The weather in {city_name} is {weather} with a temperature of {temp} degrees Celsius."
        speak(msg)
    except Exception as e:
        speak(f"Sorry, I couldn't get the weather. {e}")

reminders = []  # List of (time, message) tuples
alarms = []     # List of (time, message) tuples

def schedule_reminder(reminder_time, message):
    reminders.append((reminder_time, message))
    speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}: {message}")

def schedule_alarm(alarm_time, message):
    alarms.append((alarm_time, message))
    speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")

def reminder_checker():
    while True:
        now = datetime.datetime.now()
        # Check reminders
        for r in reminders[:]:
            if now >= r[0]:
                speak(f"Reminder: {r[1]}")
                reminders.remove(r)
        # Check alarms
        for a in alarms[:]:
            if now >= a[0]:
                speak(f"Alarm! {a[1] if a[1] else ''}")
                alarms.remove(a)
        time.sleep(30)

# Start the reminder checker in a background thread
threading.Thread(target=reminder_checker, daemon=True).start()

# Helper to parse time from string (very basic)
def parse_time_from_string(text):
    import re
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text, re.IGNORECASE)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    ampm = match.group(3)
    if ampm:
        if ampm.lower() == 'pm' and hour != 12:
            hour += 12
        elif ampm.lower() == 'am' and hour == 12:
            hour = 0
    now = datetime.datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target < now:
        target += datetime.timedelta(days=1)
    return target