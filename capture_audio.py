import pyaudio
import socketio
import time
import threading

# SocketIO client setup
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1, reconnection_delay_max=5)

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def connect_error(data):
    print("Connection failed")

sio.connect('http://localhost:5000', namespaces=['/'])

# Audio recording setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()

def record_audio():
    print("Recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    return b''.join(frames)

def send_heartbeat():
    while True:
        sio.emit('heartbeat', {'status': 'alive'}, namespace='/')
        time.sleep(10)

# Start heartbeat thread
threading.Thread(target=send_heartbeat, daemon=True).start()

while True:
    audio_data = record_audio()
    sio.emit('audio_message', audio_data, namespace='/')
    time.sleep(2)
