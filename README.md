# 🎤 ERIC: Voice Assistant with Advanced Speech Control

An intelligent voice assistant that combines speech recognition with Google GenAI to help you interact with your system using natural voice commands.

---

## ✨ Key Features

### 🎯 **Application Control**
Control your applications hands-free with natural voice commands:
- `open [app_name]` – Launch any installed application
- `close [app_name]` – Close an application
- `next app` / `switch app` / `alt tab` – Switch to the next open window
- `previous app` / `last app` – Go back to the previous window
- `switch to [app_name]` – Jump directly to a specific application
- `list apps` / `show windows` – Display all open windows
- `type [text]` – Type text directly into the focused application

### 📝 **Reminders & Scheduling**
Never forget important tasks:
- `remind me to [task] at [time]` – Set a reminder
  - Examples: `remind me to take medicine at 20:30`
  - Or: `remind me to call mom at 15:00`
  - Time format: Use HH:MM (24-hour), or specify minutes from now
- Reminders persist across restarts and run silently in the background
- Assistant speaks your reminder aloud when the time arrives

### 📖 **Screen Reader / OCR**
Perfect for accessibility and quick information gathering:
- `read screen` – Automatically screenshot, perform OCR, and speak the text aloud
- Powerful for:
  - Helping visually impaired users
  - Multitasking while reading content
  - Quickly understanding what's on screen

### 🌐 **Translation**
Quick language translation without opening browsers:
- `translate [text] to [language_code]`
  - Examples: `translate hello to es` (Spanish), `translate bonjour to en` (English)
- Supports all major languages with 2-letter language codes

### 🎵 **Media Controls**
Control your music and volume without touching the keyboard:
- **Play Music:**
  - `play song [song_name]` – Search and play on YouTube
  - `play spotify [song_name]` – Play on Spotify (launches app if available)
- **Volume Control:**
  - `volume up` / `increase volume`
  - `volume down` / `decrease volume`
- **Playback Controls:**
  - `next track` / `next song` – Skip to the next track
  - `previous track` / `previous song` / `last song` – Play the previous track
  - `pause music` / `play music` / `play` / `pause` – Toggle play/pause

### 📖 **Typing Assistance**
Helps you type anywhere without touching your keyboard:
- `start typing` – starts typing the spoken text
- `stop typing` – stops the typing

### 🔍 **AI Q&A & Search**
Ask any question and get instant, concise answers:
- For unrecognized commands, the assistant uses Google GenAI to provide quick, 1-2 line answers
- Examples: `what is the capital of France?`, `how do I learn Python?`
- Powered by Google Gemini API for intelligent responses

### 🛑 **Assistant Control**
Manage the assistant's operation:
- `rest` / `stop listening` – Pause the assistant and enter standby mode (only responds to "Eric" wake word)
- `eric` – Wake up a paused assistant
- `exit` – Gracefully exit the application

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Windows operating system (for window management features)
- Microphone and speakers

### Step 1: Install Python Dependencies
```powershell
pip install pyautogui pytesseract pillow googletrans==4.0.0-rc1 speech-recognition pyttsx3 google-genai psutil
```

### Step 2: Install Tesseract OCR
For the screen reader feature, install Tesseract OCR:
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and remember the installation path
3. Add it to your system PATH or update the path in the code if needed

### Step 3: Set Up Google GenAI API Key
1. Get your API key from: https://aistudio.google.com/
2. Add the key to the `search()` function in `functions.py`:
```python
API_KEY = "YOUR_API_KEY_HERE"
```

### Step 4: Configure Authentication

The system supports two authentication methods. Choose one or both based on your preference.

#### Option A: Face Authentication Setup (Recommended for Hands-Free Use)
Face authentication uses OpenCV and facial recognition. To set it up:

1. **Train your face model:**
   ```bash
   python auth/trainer.py
   ```
   - When prompted, enter your identifier number (e.g., `1` for first user, `2` for second, etc.)
   - Position your face in front of the camera
   - The system will capture multiple samples and train the model
   - The trained model is saved to `auth/trainer/trainer.yml`

2. **Update user names in `auth/recognize.py`:**
   ```python
   id = 2  # Update this to the number of users
   names = ['', 'Your Name', 'Another User']  # Add your name at the correct position
   ```

3. **For Multiple Users:**
   - Each user runs `python auth/trainer.py` with a unique ID
   - Update the `id` and `names` list accordingly
   - The system will recognize any trained user

#### Option B: Password Authentication
1. **Set your password in `auth/pswd.py`:**
   ```python
   PASSWORD = 'your_secure_password'
   ```

2. **Optional: Customize the authentication window**
   - Replace `auth/img.png` with your own image (300x250 pixels recommended)
   - Modify colors and styling in the `ask_password()` function

---

## 🔐 Authentication Details

### Security Considerations
- **Face Auth:** Only allows trained faces to access the system. No network transmission occurs.
- **Password Auth:** Uses a simple password verification. For better security, update the password to a strong one.
- **For Multiple Users:** Each user has their own trained face model or password stored locally.

### Switching Authentication Methods in Code
Edit `voiceAssistance.py` to change the authentication flow:
```python
# Line 7-13: Modify the authentication request to prefer one method
speak("""Verification needed. How would you like to verify yourself?
       1. Face Authentication. 2. Password""")
```

---

## 📖 Usage

### Basic Usage
```bash
python voiceAssistance.py
```

The assistant will:
1. Perform verification (face auth or password if enabled)
2. Greet you based on time of day
3. Listen for your voice commands
4. Execute the command and provide feedback

### Example Commands

**Application Control:**
```
"Open Chrome"
"Switch to Visual Studio Code"
"Next app"
"List windows"
```

**Reminders:**
```
"Remind me to take medicine at 20:30"
"Remind me to call john at 14:00"
```

**Screen Reading:**
```
"Read screen"
```

**Translation:**
```
"Translate hello to es"
"Translate bonjour to de"
```

**Music Control:**
```
"Play song Blinding Lights"
"Play spotify Bohemian Rhapsody"
"Volume up"
"Next track"
```

**Question Answering:**
```
"What is the capital of France?"
"How do I learn machine learning?"
"Tell me about artificial intelligence"
```

**Assistant Control:**
```
"Rest" / "Stop listening" – Pause the assistant (say "Eric" to resume)
"Exit" – Exit the assistant application
```

---

## 📁 Project Structure

```
speechDetector/
├── voiceAssistance.py      # Main voice assistant loop
├── functions.py             # Core functions (speech recognition, search, greetings)
├── assistant_ext.py         # Extended features (reminders, OCR, translation, app switching)
├── auth/                    # Authentication module
│   ├── authentication.py    # Main auth logic
│   ├── recognize.py         # Face recognition using OpenCV
│   ├── pswd.py              # Password authentication GUI
│   ├── trainer.py           # Script to train face recognition model
│   ├── trainer/             # Face model storage (auto-generated)
│   │   └── trainer.yml      # Trained face recognition model
│   ├── samples/             # Face training samples directory
│   ├── haarcascade_frontalface_default.xml  # Haar cascade for face detection
│   ├── img.png              # Authentication window image
│   └── __pycache__/
├── reminders.json           # Saved reminders (auto-generated)
└── README.md
```

---

## 🔧 Configuration

### Voice Properties
In `functions.py`, customize voice settings:
```python
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)        # Speed (0-300)
    engine.setProperty('volume', 1.0)      # Volume (0.0-1.0)
```

### API Keys
- **Google GenAI:** Set in `functions.py` search() function
- **Tesseract Path:** Edit in `assistant_ext.py` if not in system PATH

### Reminder Persistence
Reminders are automatically saved to `reminders.json` and loaded on startup.

---

## 👥 Setup for Multiple Users

This assistant can be configured for multiple users with separate authentication credentials. Each user has their own voice identity and settings.

### Step 1: Face Authentication for Each User
Each user must run the face training script individually:

```bash
# User 1 runs:
python auth/trainer.py
# When prompted, enters: 1
# Captures their face samples

# User 2 runs:
python auth/trainer.py
# When prompted, enters: 2
# Captures their face samples

# And so on...
```

### Step 2: Update User Configuration
Edit `auth/recognize.py` to register all users:

```python
id = 3  # Total number of users

# Add each user's name in order
names = ['', 'Samyak', 'John', 'Alice']
#           ID:1      ID:2    ID:3
```

### Step 3: Customize Per-User Settings (Optional)
To personalize greetings for each user, you can modify `functions.py`:
- Each user can have their own reminders in `reminders.json`
- Reminders are listed with timestamps and checked on startup
- Voice preferences (rate, volume) can be set per user if desired

### Alternative: Password Authentication for Multiple Users
If you prefer password authentication:

1. Create a credentials file `auth/users.py`:
```python
USERS = {
    'samyak': 'secure_password_1',
    'john': 'secure_password_2',
    'alice': 'secure_password_3'
}
```

2. Update `pswd.py` to accept usernames and check against the credentials file:
```python
from auth.users import USERS

def ask_password():
    # Modify to ask for username first, then password
    # Check credentials against USERS dictionary
    ...
```

---

## 🎯 Keyboard Shortcuts Used

| Command | Shortcut |
|---------|----------|
| Next App | Alt + Tab |
| Previous App | Shift + Alt + Tab |
| Open Application | Windows + Type + Enter |
| Close Window | Alt + F4 |

---

## 💡 Future Enhancements

Potential features for future development:

1. **Meeting Summarizer** – Record meetings, transcribe, and summarize automatically
2. **Smart Home Integration** – Control lights, appliances via MQTT/Home Assistant
3. **Document Assistant** – Open files, search content, edit passages hands-free
4. **Offline Mode** – Switch to local speech models for privacy
5. **Calendar Integration** – Check and create events by voice
6. **Email Management** – Read and send emails by voice
7. **Custom Commands** – User-defined voice macros and shortcuts

---

## 📝 Technical Notes

### Modular Design
Features are split into separate modules:
- `functions.py` – Core functionality
- `assistant_ext.py` – Extended features (easily add new functions)
- `voiceAssistance.py` – Command parsing and execution

This makes it easy to add new features without modifying core logic.

### Threading
- Reminders run in a background daemon thread
- Doesn't block the main listening loop
- Automatically cleaned up on exit

### Error Handling
- Graceful fallback if services are unavailable
- User-friendly error messages via speech
- Continues operating after errors

---

## ⚠️ Privacy & Security

- Speech recognition uses Google's Speech-to-Text service
- Questions/answers use Google GenAI (sends text to Google)
- Reminders and local data stored in `reminders.json`
- No audio recording or storage by default
- Consider network privacy when using API-based features

---

## 🐛 Troubleshooting

### Authentication Issues

#### Face Authentication Not Working
- **Webcam not detected:** Ensure your webcam is connected, enabled, and not in use by other applications
- **Model file not found:** Run `python auth/trainer.py` to create the trained model (`trainer/trainer.yml`)
- **"trainer.yml" file missing:** The trained face model doesn't exist. Train your face first using the trainer script
- **Face not recognized:** 
  - Ensure adequate lighting in the environment
  - Make sure your face is clearly visible and within the camera frame
  - Re-train your face model if recognition is consistently failing
  - Update your user ID in `auth/recognize.py` if you're a new user

#### Password Authentication Popup Not Appearing
- Check if `auth/img.png` exists; if not, create a placeholder image or comment out the image line
- Ensure tkinter is installed: `pip install tk`
- Verify the window coordinates work on your display resolution

#### "Verification needed" Prompt Issues
- **Microphone not working:** Check if it's enabled and other apps aren't using it
- **Speech not recognized:** Speak clearly and choose option 1 or 2 explicitly
- Valid commands: "face authentication", "password", "one", "two", "first", "second"

---

### Microphone not detected
- Ensure microphone is connected and enabled in Windows Sound Settings
- Check if another application is using the microphone

### Speech recognition not working
- Verify internet connection (required for Google Speech-to-Text)
- Check microphone levels and ambient noise

### Application switching not working
- Ensure the application window is visible
- Try `list apps` to see available windows
- Use partial app names if exact name doesn't match

### API errors
- Verify your Google GenAI API key is correct and active
- Check internet connectivity
- Ensure rate limits are not exceeded

---

## 📄 License

Personal project for learning and productivity enhancement.

---

## 🙏 Acknowledgments

Built with:
- **SpeechRecognition** – Speech-to-text
- **pyttsx3** – Text-to-speech
- **Google GenAI** – AI responses
- **Tesseract OCR** – Screen reading
- **pyautogui** – System automation
- **win32gui** – Window management

---

**Happy assisting! 🎉**
