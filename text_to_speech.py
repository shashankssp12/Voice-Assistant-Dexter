import os
import shutil
import subprocess
import time
import requests

class TextToSpeech:
    # Set your Deepgram API Key and desired voice model
    DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    MODEL_NAME = "aura-helios-en"  # Example model name, change as needed

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        return lib is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&performance=some&encoding=linear16&sample_rate=24000"
        headers = {
            "Authorization": f"Token {self.DG_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

        player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
        player_process = subprocess.Popen(
            player_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        start_time = time.time()  # Record the time before sending the request
        first_byte_time = None  # Initialize a variable to store the time when the first byte is received

        with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    if first_byte_time is None:  # Check if this is the first chunk received
                        first_byte_time = time.time()  # Record the time when the first byte is received
                        ttfb = int((first_byte_time - start_time)*1000)  # Calculate the time to first byte
                        print(f"TTS Time to First Byte (TTFB): {ttfb}ms\n")
                    player_process.stdin.write(chunk)
                    player_process.stdin.flush()

        if player_process.stdin:
            player_process.stdin.close()
        player_process.wait()
