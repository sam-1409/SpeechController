import speech_recognition as sr
from auth.pswd import ask_password
from auth import recognize
from functions import speak
        
def ask_for_authentication():
    print("say")
    r = sr.Recognizer()
    flag = 0
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        if(text.lower() in ['face authentication', 'authentication', 'first one', 'one', 'first']):
            flag = recognize.AuthenticateFace()
            return flag
        elif(text.lower() in ['password', 'second one', 'two', 'second']):
            flag = ask_password()
            return flag
        else:
            speak("choose a valid option")
            return -1
    except sr.UnknownValueError:
            speak("Could not understand audio")