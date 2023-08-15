from google.cloud import texttospeech_v1 as texttospeech
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

client = texttospeech.TextToSpeechClient()

voices = client.list_voices()

for voice in voices.voices:
    language_code = voice.language_codes[0]
    if language_code.startswith('en-US') or language_code.startswith('en-GB'):
        print(f'Name: {voice.name}')
        print(f'Language Code: {language_code}')
        print(f'Gender: {voice.ssml_gender}')
        print(f'Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}')
        print('')
