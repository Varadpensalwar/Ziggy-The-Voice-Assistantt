import os
import eel
import threading

from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():
    eel.init("www")
    playAssistantSound()
    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
            # Start hotword detection in a background thread
            threading.Thread(target=hotword_listener, daemon=True).start()
        else:
            speak("Face Authentication Fail")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)

# Hotword listener that triggers allCommands when hotword is detected
def hotword_listener():
    from engine.features import hotword
    hotword(trigger_callback=allCommands)