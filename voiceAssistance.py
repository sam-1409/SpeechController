import pyautogui as pg
from auth.authentication import ask_for_authentication
from functions import *
from datetime import datetime, timedelta
from assistant_ext import *

speak("""Verification needed. How would you like to verify yourself
       1. Face Authentication. 2. Password""") 

#Authentication loop
flag = ask_for_authentication()
while flag != 1:
    if flag!=-1:
        speak("User not verified")
    flag = ask_for_authentication()

speak("Verification completed.")
print("Verification completed")

check_reminders(lambda text: speak(f"Reminder: {text}"))
greet()

listening = True

while True:
    text = speechToText()
    if text is None:
        continue
    
    if not listening:
        if text.lower() == "eric":
            listening = True
            greet()
        continue

    if text.lower() == 'exit':
        speak('Exiting! Have a good day')
        break

    elif text.lower() == 'rest' or text.lower() == 'stop listening':
        listening = False
        speak("Assistant paused. Say 'Eric' to wake me up.")
        
    elif text.lower().startswith('open '):
        app = text.lower()[5:]
        speak(f'opening {app}')
        try:
            pg.press('win')
            pg.typewrite(app)
            time.sleep(1)
            pg.press('enter')
        except Exception:
            speak("Application not found")
            
    elif text.lower().startswith('type '):
        write = text.lower()[5:]
        speak('typing')
        pg.typewrite(write)
        pg.press('enter')
        
    elif text.lower().startswith('close '):
        app = text.lower()[6:]
        speak(f'closing {app}')
        pg.hotkey('alt', 'f4')
        
    # new features
    elif text.lower().startswith('remind me to '):
        # expected format: remind me to <task> at <time>
        try:
            parts = text.lower().split('remind me to ')[1]
            if ' at ' in parts:
                task, when = parts.rsplit(' at ', 1)
                # try parse absolute time, else assume in minutes
                when_dt = None
                try:
                    when_dt = datetime.fromisoformat(when)
                except Exception:
                    # try hh:mm today
                    try:
                        now = datetime.now()
                        h,m = when.split(':')
                        when_dt = now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
                        if when_dt < now:
                            when_dt += timedelta(days=1)
                    except Exception:
                        # fallback: minutes
                        delta = int(when)
                        when_dt = datetime.now() + timedelta(minutes=delta)
                set_reminder(task, when_dt)
                speak(f'Reminder set for {task} at {when_dt}')
            else:
                speak("Please tell me when to remind you, for example 'remind me to buy milk at 14:00'")
        except Exception:
            speak("Couldn't set reminder. Try again.")

    elif text.lower() == 'read screen' or text.lower() == 'screen read':
        speak('Reading screen now')
        try:
            content = read_screen()
            if content.strip():
                speak(content)
            else:
                speak('No text found on screen')
        except Exception as e:
            speak('Failed to read screen')

    elif text.lower().startswith('translate '):
        try:
            # format: translate <text> to <lang>
            body = text[10:]
            if ' to ' in body:
                txt, lang = body.rsplit(' to ',1)
                translated = translate(txt, dest_lang=lang)
                speak(translated)
            else:
                speak('Specify target language e.g. translate hello to es')
        except Exception:
            speak('Translation error')

    # media controls
    elif text.lower().startswith('play song '):
        song = text[10:]
        speak(f'Playing {song}')
        play_song(song)  # default youtube

    elif text.lower().startswith('play spotify '):
        song = text[13:]
        speak(f'Opening spotify search for {song}')
        play_song(song, platform='spotify')

    elif text.lower() in ('volume up', 'increase volume'):
        volume_up()
        speak('Volume increased')
    elif text.lower() in ('volume down', 'decrease volume'):
        volume_down()
        speak('Volume decreased')

    elif text.lower() in ('next track', 'next song'):
        next_track()
        speak('Skipped to next track')
    elif text.lower() in ('previous track', 'previous song', 'last song'):
        previous_track()
        speak('Playing previous track')

    elif text.lower() in ('pause music', 'play', 'play music', 'pause'):
        play_pause()
        speak('Toggled play/pause')

    # app switching
    elif text.lower() in ('next app', 'switch app', 'alt tab'):
        if switch_next_app():
            speak('Switched to next application')
        else:
            speak('Failed to switch application')
    
    elif text.lower() in ('previous app', 'last app'):
        if switch_previous_app():
            speak('Switched to previous application')
        else:
            speak('Failed to switch application')
    
    elif text.lower().startswith('switch to '):
        app = text[10:].strip()
        if switch_to_app_by_name(app):
            speak(f'Switched to {app}')
        else:
            speak(f'Could not find application {app}')
    
    elif text.lower() in ('list apps', 'show apps', 'list windows', 'show windows'):
        windows = get_open_windows()
        if windows:
            app_list = ', '.join([w['title'][:30] for w in windows[:10]])  # limit to 10
            speak(f'You have {len(windows)} windows open. Here are some: {app_list}')
            print("Open windows:")
            for i, w in enumerate(windows, 1):
                print(f"  {i}. {w['title']} ({w['process']})")
        else:
            speak('No open windows found')

    elif text.lower() in ('new tab', 'open new tab'):
        pg.hotkey('ctrl', 't')
        speak('Opened new tab')
    
    elif text.lower() in ('close tab', 'close current tab'):
        pg.hotkey('ctrl', 'w')
        speak('Closed current tab')
        
    elif text.lower() in ('next tab', 'switch tab', 'previous tab', 'last tab'):
        if 'next' in text.lower() or 'switch' in text.lower():
            pg.hotkey('ctrl', 'tab')
            speak('Switched to next tab')
        else:
            pg.hotkey('ctrl', 'shift', 'tab')
            speak('Switched to previous tab')     
    
    elif text.lower() == 'start typing':
        speak('Start typing now. Say "stop typing" to stop.')
        while True:
            t = speechToText()
            if t is None:
                continue
            if t.lower() == 'stop typing':
                speak('Stopped typing')
                break
            pg.typewrite(t + ' ')
                
    else:
        try:
            prompt = text
            response = search(prompt)
            speak(response)
        except Exception as e:
            print(f"Unexpected error in search: {e}")
            speak("I encountered an error while processing your request. Please try again.")