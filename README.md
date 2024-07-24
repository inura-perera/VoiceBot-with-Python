# Python Voice Chat Bot

This is a Python-based multilingual voice chat bot powered by Google Gemini and various Python libraries. It supports English and Chinese and can engage in conversations by recognizing speech, generating responses, converting text to speech, and playing audio.

## Features

- Multilingual support 
- Speech recognition using `speech_recognition`
- Text generation using Google Gemini API
- Text-to-speech using `gtts`
- Audio playback using `pygame`
- Asynchronous handling of text generation, TTS, and audio playback using multithreading

## Requirements

- Python 3.12 or higher
- Google Gemini API key

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/voice-chat-bot.git
    cd voice-chat-bot
    ```

2. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -q -U google-generativeai    
    pip install speechrecognition openai pyttsx3 pyaudio pygame
    pip install setuptools
    ```

4. Make sure to replace placeholders like `your_google_gemini_api_key` with actual values.

    ```python
    
    API_KEY = 'your_google_gemini_api_key'
    ```

5. Ensure your microphone is working and accessible.

## Usage

Run the script:

```sh
python voice_chat_bot.py


