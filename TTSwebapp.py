import streamlit as st
from google.cloud import texttospeech_v1 as texttospeech
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Custom CSS to set background color and other styles
st.markdown("""
    <style>
        body {
            background-color: #f0f0f5;
        }
    </style>
    """, unsafe_allow_html=True)

# Set up Google TTS client
client = texttospeech.TextToSpeechClient()
# Container for centering content
with st.container():
    # Title of the web app
    st.title('Text to Speech Converter')
    st.subheader('Using Google Text-to-Speech API')

    # List of available voices
    voices = [
        "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Standard-F",
        "en-US-Standard-A", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E",
        "en-US-Standard-F", "en-US-Standard-G", "en-US-Standard-H", "en-US-Standard-I", "en-US-Standard-J",
        "en-GB-News-G", "en-GB-News-H", "en-GB-News-I", "en-GB-News-J", "en-GB-News-K",
        "en-GB-News-L", "en-GB-News-M", "en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C",
        "en-GB-Wavenet-D", "en-GB-Wavenet-F", "en-US-News-K", "en-US-News-L", "en-US-News-M",
        "en-US-News-N", "en-US-Wavenet-G", "en-US-Wavenet-H", "en-US-Wavenet-I", "en-US-Wavenet-J",
        "en-US-Wavenet-A", "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E",
        "en-US-Wavenet-F", "en-US-Studio-M", "en-US-Studio-O", "en-GB-Neural2-A", "en-GB-Neural2-B",
        "en-GB-Neural2-C", "en-GB-Neural2-D", "en-GB-Neural2-F", "en-US-Neural2-A", "en-US-Neural2-C",
        "en-US-Neural2-D", "en-US-Neural2-E", "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H",
        "en-US-Neural2-I", "en-US-Neural2-J", "en-US-Polyglot-1"
    ]
    
    # Create a selection box with the voices
    selected_voice = st.selectbox('Choose a voice:', voices)
    
    # Display the selected voice
    st.write(f"You selected voice: {selected_voice}")

    # Speed control
    speed_rate = st.slider('Speed rate:', min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    # Pitch control
    pitch = st.slider('Pitch:', min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

    # Get user input
    user_input = st.text_area('Enter the text you want to convert to speech:')

    # Create a button to trigger speech conversion
    if st.button('Convert Text to Speech'):
        if user_input.strip() == "":
            st.warning('Please enter some text.')
        else:
            # Build the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=user_input)

            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=selected_voice.split('-')[0] + '-' + selected_voice.split('-')[1],
                name=selected_voice,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

            # Select the type of audio file you want
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speed_rate,
                pitch=pitch)

            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config)

            # Save the response to an audio file
            audio_file = 'output.mp3'
            with open(audio_file, 'wb') as out:
                out.write(response.audio_content)

            # Embed the audio file in the web app
            st.audio(audio_file)

            st.success('Audio has been generated successfully!')

    # Reset button
    if st.button('Reset'):
        st.experimental_rerun()

    # About and Help sections
    with st.expander("About"):
        st.markdown('This web application utilizes the Google Text-to-Speech API to convert the text you input into speech. It is built with Streamlit and can be customized further to include additional functionality.')

    with st.expander("Documentation"):
        st.markdown('[User Guide](https://example.com/user_guide.pdf)')
        st.markdown('[FAQs](https://example.com/faqs.html)')

    with st.expander("Help & FAQs"):
        st.markdown('Frequently asked questions and support.')
