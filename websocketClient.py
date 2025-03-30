import asyncio
import websockets
import cv2
import numpy as np
import threading
import time 
import pyttsx3

class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

url = "ws://10.25.248.243:8765"  # Server address

# tts = pyttsx3.init()
# tts.setProperty('rate', 160)  # Adjust speech speed for better clarity

# speech_lock = threading.Lock()

def speak_description(description):
    # with speech_lock:  # Ensure only one thread accesses speech synthesis at a time
    # try:
    #     print("Thread called:", description)
    #     tts.say(description)
    #     tts.runAndWait()
    # except RuntimeError:
    #     pass
        # do nothing i.e. dont speak
    tts = _TTS()
    tts.start(description)
    del(tts)
        


# connect to server
async def send_frame():
    target_fps = 10  # Desired FPS
    frame_delay = 1.0 / target_fps
    last_time = time.time()
    async with websockets.connect(url) as websocket:
        cap = cv2.VideoCapture(0)
        while True:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())  # Send raw bytes

            speech = await websocket.recv()
            if speech != "":
                print("calling thread:", speech)
                threading.Thread(target=speak_description, args=(speech,)).start()
            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, frame_delay - elapsed_time))
        cap.release()
# Run the client
asyncio.run(send_frame())
