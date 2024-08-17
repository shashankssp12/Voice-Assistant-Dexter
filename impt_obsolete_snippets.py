# DEEPGRAM_URL = "https://api.deepgram.com/v1/speak?model=aura-orpheus-en"


# def save_response_as_audio(response):
    # print("Dexter: " + response)
    # payload = {
    #     "text": response 
    #         }

    # headers = {
    #     "Authorization": f"Token {DEEPGRAM_API_KEY}",
    #     "Content-Type": "application/json"
    # }

    # audio_file_path = "output_TTS.wav"  # Path to save the audio file

    # with open(audio_file_path, 'wb') as file_stream:
    #     response = requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True)
    #     for chunk in response.iter_content(chunk_size=1024):
    #         if chunk:
    #             file_stream.write(chunk) # Write each chunk of audio data to the file
    # print("Audio download complete")

    # # Play the audio file
    # audio = AudioSegment.from_file(audio_file_path)
    # play(audio)

    # # Delete the audio file after playback
    # os.remove(audio_file_path)
    # print("Audio file deleted")