import speech_recognition as sr
import google.generativeai as genai
import google.api_core.exceptions
import pyttsx3
import time
import random
from assistant_ext import set_reminder, check_reminders, read_screen, translate

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
def greet():
    t = time.localtime()
    hour = t.tm_hour

    prefix = ""
    if 5 <= hour < 12:
        prefix = "Good morning Samyak, "
    elif 12 <= hour < 16:
        prefix = "Good afternoon Samyak, "
    elif 16 <= hour < 20:
        prefix = "Good evening Samyak, "
    else:
        prefix = "Hello Samyak, "
        
    message = [
        "how can I help you?",
        "need some assistance?", 
        "what is in your mind?",
        "what can I do for you?"
    ]
    
    greeting_message = prefix + random.choice(message)
    speak(greeting_message)
    
def search(prompt):
    if 5 < len(prompt) < 200:
        const = ". give response with to the point precision in 1 to 2 lines."
        API_KEY = "AIzaSyDskvlAV8Z5_zeK9nFvYtnO8VeyHCKufpk"
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        try:
            response = model.generate_content(prompt + const)
            print(response.text)
            return response.text
        except google.api_core.exceptions.ResourceExhausted:
            error_msg = "API quota exceeded. Please try again later or upgrade your plan."
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error calling API: {str(e)}"
            print(error_msg)
            return error_msg
    else:
        return "Could not understand your question"
    
def speechToText():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    
    except sr.UnknownValueError:
        speak("Could not understand audio")
    
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")