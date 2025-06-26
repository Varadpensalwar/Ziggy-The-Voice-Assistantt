# Ziggy - The Voice Assistant

Ziggy is an open-source, voice-controlled personal assistant designed to enhance productivity and provide a seamless user experience. This project enables users to perform various tasks through natural voice commands, featuring advanced capabilities like face authentication and hotword detection. Ziggy can execute multiple commands including opening applications, playing YouTube videos, making calls, and sending messages.

## Features

- **Face Authentication**: Secure access with facial recognition
- **Hotword Detection**: Activate the assistant using keywords like "jarvis" or "alexa"
- **Voice Commands**: Control your computer and perform tasks using voice
- **Web Integration**: Open websites and search the internet
- **Application Control**: Launch applications on your system
- **YouTube Integration**: Play videos directly from voice commands
- **WhatsApp Integration**: Send messages and make calls via WhatsApp
- **Android Integration**: Control your Android device (requires ADB)
- **AI Chatbot**: Get responses to questions using HugChat

## Installation

### Prerequisites
- Python 3.6 or higher
- Windows operating system
- Microsoft Edge browser
- Android device and ADB (for mobile features)

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/Varadpensalwar/Ziggy-The-Voice-Assistantt.git
   cd Ziggy-The-Voice-Assistantt
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   If no requirements.txt is available, install the following packages:
   ```bash
   pip install eel playsound pyaudio pyautogui pywhatkit pvporcupine hugchat
   ```

3. Set up the database:
   The application uses SQLite for storing contacts and commands. The database file `ziggy.db` is included in the repository.
   
4. Configure face authentication:
   Follow the instructions in the [Authentication Setup](#authentication-setup) section below.

## Usage

1. Run the assistant:
   ```bash
   python run.py
   ```

2. The system will start and wait for face authentication
3. After successful authentication, you can use voice commands to control the assistant
4. Use the hotword "jarvis" or "alexa" to activate the assistant

## Authentication Setup

Ziggy uses facial recognition for secure access. To set up authentication:

1. Navigate to the authentication directory:
   ```bash
   cd engine/auth
   ```

2. Run the trainer script to create your facial profile:
   ```bash
   python trainer.py
   ```

3. Follow the on-screen instructions to complete the face scanning process

Once configured, Ziggy will recognize your face when you start the application.

## Project Structure

```
Ziggy-The-Voice-Assistantt/
├── main.py                 # Main application file that initializes the UI and authentication
├── run.py                  # Entry point that starts the assistant and hotword detection processes
├── device.bat              # Batch file for device initialization
├── ziggy.db                # SQLite database for contacts and commands
├── engine/                 # Core functionality directory
│   ├── features.py         # Main features implementation
│   ├── command.py          # Voice command processing
│   ├── config.py           # Configuration settings
│   ├── helper.py           # Helper functions
│   ├── db.py               # Database operations
│   └── auth/               # Authentication related files
│       ├── recoganize.py   # Face recognition implementation
│       ├── trainer.py      # Face profile training
│       └── sample.py       # Sample collection
└── www/                    # Web interface files
    ├── index.html          # Main UI
    ├── assets/             # Static assets
    │   ├── audio/          # Sound files
    │   ├── css/            # Stylesheets
    │   ├── js/             # JavaScript files
    │   └── images/         # Image resources
    └── ...
```

Each component is designed to be modular, making it easy to extend or modify the functionality of Ziggy.

## Voice Commands

Ziggy responds to a variety of voice commands. Here are some examples:

| Command | Description | Example |
|---------|-------------|---------|
| Open [application/website] | Opens the specified application or website | "Open Chrome" or "Open YouTube" |
| Play [song/video] on YouTube | Searches and plays the specified content on YouTube | "Play Despacito on YouTube" |
| Send a message to [contact] | Sends a WhatsApp message to the specified contact | "Send a message to John" |
| Call [contact] | Makes a call to the specified contact | "Call Mom" |
| Video call [contact] | Initiates a video call with the specified contact | "Video call Sarah" |
| Ask [question] | Uses the AI chatbot to answer questions | "Ask what is the capital of France" |

You can extend Ziggy's capabilities by adding new commands in the `engine/command.py` file.

## Technical Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 10 or 11 |
| Python | Version 3.6 or higher |
| Browser | Microsoft Edge |
| Mobile Integration | Android device with USB debugging enabled |
| Development | ADB (Android Debug Bridge) for Android integration |
| Storage | Minimum 100MB free space |
| RAM | Minimum 4GB recommended |

## License

This project is released under the MIT License, making it freely available for both personal and commercial use, modification, and distribution.

## Contributing

Contributions are welcome and encouraged! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate documentation.

## Community and Support

- **Issues**: Report bugs or request features through [GitHub Issues](https://github.com/Varadpensalwar/Ziggy-The-Voice-Assistantt/issues)
- **Discussions**: Join the conversation about Ziggy's development and usage
- **Updates**: Star and watch the repository to stay informed about updates

## Roadmap

The Ziggy Voice Assistant project is under active development. Here are some planned features for future releases:

- **Multi-language Support**: Adding support for multiple languages beyond English
- **Custom Wake Words**: Allowing users to set their own wake words
- **Cloud Sync**: Syncing settings and data across multiple devices
- **Smart Home Integration**: Connecting with popular smart home platforms
- **Advanced NLP**: Implementing more sophisticated natural language processing
- **Cross-platform Support**: Extending compatibility to macOS and Linux

## Acknowledgements

- This project uses [HugChat](https://github.com/Soulter/hugging-chat-api) for AI-powered conversations
- Voice recognition powered by [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- Hotword detection implemented with [Porcupine](https://github.com/Picovoice/porcupine)
- UI built with [Eel](https://github.com/ChrisKnott/Eel)

---

<p align="center">
  <i>Made with ❤️ by <a href="https://github.com/Varadpensalwar">Varad Pensalwar</a></i>
</p>