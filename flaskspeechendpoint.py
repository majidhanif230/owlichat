from flask import Flask, request, jsonify
from google.cloud import texttospeech, speech_v1p1beta1 as speech
from your_model_library import GenerativeModel  # Import your generative model library

app = Flask(__name__)

# Initialize Text-to-Speech client
tts_client = texttospeech.TextToSpeechClient()
# Initialize Speech-to-Text client
stt_client = speech.SpeechClient()
# Initialize your generative model
generative_model = GenerativeModel()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input')

    # Assume GenerativeModel has a method `generate_response`
    try:
        ai_response = generative_model.generate_response(user_input)  # Replace this with the correct method
    except AttributeError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": ai_response})

@app.route('/voice_to_text', methods=['POST'])
def voice_to_text():
    audio_file = request.files['audio']
    audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = stt_client.recognize(config=config, audio=audio)
    transcription = response.results[0].alternatives[0].transcript

    return jsonify({"text": transcription})

@app.route('/text_to_voice', methods=['POST'])
def text_to_voice():
    data = request.json
    text = data.get('text')

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content, 200, {'Content-Type': 'audio/mpeg'}

if __name__ == '__main__':
    app.run(debug=True)
