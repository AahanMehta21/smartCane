import asyncio
import websockets
import cv2
import time
import subprocess
import os

class _TTS:
    def __init__(self):
        # Pico TTS command
        self.pico_path = "/usr/bin/pico2wave"  # Path to pico2wave (ensure this is correct)
        self.play_path = "/usr/bin/aplay"      # Path to aplay (ensure this is correct)
        self.current_speech = "None"  # To track the current speech text
        self.audio_file = None      # To store the path of the generated audio file
        self.play_process = None    # To track the current audio process

    async def start(self, text_):
        # Check if the text is the same as the current speech
        if text_.strip() != self.current_speech.strip():
            # If different, stop the previous speech if it's playing
            if self.play_process is not None:
                print("Stopping previous speech.")
                await self.stop_audio()

            # Update the current speech and generate new audio
            self.current_speech = text_
            self.audio_file = self.generate_audio(text_)
            await self.play_audio()

    def generate_audio(self, text_):
        # Generate the speech file using pico2wave
        wave_file = "/tmp/speech.wav"
        subprocess.run([self.pico_path, "-w", wave_file, text_])
        return wave_file

    async def play_audio(self):
        # Play the generated speech file using aplay
        if self.audio_file:
            # Start playing the audio using subprocess asynchronously
            self.play_process = subprocess.Popen([self.play_path, self.audio_file])
            # Wait for the process to finish asynchronously using `await`
            await asyncio.to_thread(self.play_process.wait)

    async def stop_audio(self):
        # Stop the previously running aplay process if it exists
        if self.play_process is not None:
            try:
                print(f"Terminating previous audio process.")
                # Attempt to terminate the running aplay process
                self.play_process.terminate()
                # Wait asynchronously for the process to terminate
                await asyncio.to_thread(self.play_process.wait)  
                print(f"Stopped audio: {self.audio_file}")
                os.remove(self.audio_file)  # Clean up the audio file after playback
                self.audio_file = None
                self.play_process = None
            except Exception as e:
                print(f"Error stopping audio: {e}")
        else:
            print("No audio process to stop.")

# connect to server
async def send_frame():
    target_fps = 10  # Desired FPS
    frame_delay = 1.0 / target_fps
    async with websockets.connect("ws://10.25.248.243:8765") as websocket:
        cap = cv2.VideoCapture(0)
        tts = _TTS()  # Create an instance of the TTS class
        while True:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())  # Send raw bytes

            speech = await websocket.recv()
            if speech != "":
                # Only start a new TTS process if the text is different
                await tts.start(speech)

            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, frame_delay - elapsed_time))
        cap.release()

# Run the client
asyncio.run(send_frame())
