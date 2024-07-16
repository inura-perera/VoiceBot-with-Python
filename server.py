import os
import io
from flask import Flask
from flask_socketio import SocketIO
from google.cloud import speech
from google.cloud import texttospeech
import simpleaudio as sa
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Set up Google Cloud client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "speech-recognition-429514-0c5d0bd7c4cd.json"
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

GEMINI_API_KEY = 'AIzaSyCgpWR28zQkLSup50xbzYqHDFSZbfpkKKs'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)
    print("Google Speech-to-Text Response:", response)
    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return ""

def generate_response(text):
    if not text.strip():
        return "I didn't catch that. Could you please say it again?"
    
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
    
    print("Gemini API Response Status Code:", response.status_code)
    print("Gemini API Response Content:", response.content.decode('utf-8'))

    try:
        response_data = response.json()
        print("Gemini API Parsed Response:", response_data)
        if response.status_code == 200 and 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Sorry, I didn't understand that."
    except ValueError as e:
        print("Error parsing JSON response:", e)
        return "Sorry, I didn't understand that."

def synthesize_text(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content

def play_audio(audio_content):
    with open("output.wav", "wb") as out:
        out.write(audio_content)
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

@socketio.on('audio_message', namespace='/')
def handle_audio_message(data):
    print("Received audio message")
    print(f"Audio data length: {len(data)} bytes")
    transcript = transcribe_audio(data)
    print("Transcript: ", transcript)
    response_text = generate_response(transcript)
    print("Response: ", response_text)
    audio_content = synthesize_text(response_text)
    play_audio(audio_content)

@socketio.on('heartbeat', namespace='/')
def handle_heartbeat(data):
    print("Heartbeat received")

if __name__ == '__main__':
    socketio.run(app)
