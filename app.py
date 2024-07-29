from flask import Flask, request, jsonify, render_template, url_for
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import pandas as pd
import logging
from google.cloud import bigquery, speech_v1, texttospeech
from big import query_bigquery

app = Flask(__name__)

# Initialize Vertex AI and GenerativeModel
project_id = "vertext-0001"
vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")
client = bigquery.Client()

# Initialize BigQuery client
try:
    bq_client = bigquery.Client(project=project_id)
except Exception as e:
    logging.error(f"Failed to initialize BigQuery client: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load prompts once at the start of your application
prompts = query_bigquery()

# Prompt template
prompt_template = """
Now, respond to the following user input:
User: {user_input}"""

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/another_page')
def another_page():
    return render_template('redirect.html')

@app.route('/profile')
def profile():
    prompt = prompts.get('My Profile', 'Default prompt text')
    logger.info(f'Profile Prompt: {prompt}')
    return render_template('profile.html', prompt=prompt)

@app.route('/bed_ready')
def bed_ready():
    prompt = prompts.get('Bed Ready', 'Default prompt text')
    logger.info(f'Bed Ready Prompt: {prompt}')
    return render_template('bed_ready.html', prompt=prompt)

@app.route('/slumber_party')
def slumber_party():
    prompt = prompts.get('Slumber Party', 'Default prompt text')
    logger.info(f'Slumber Party Prompt: {prompt}')
    return render_template('slumber_party.html', prompt=prompt)

@app.route('/my_sounds')
def my_sounds():
    prompt = prompts.get('My Sounds', 'Default prompt text')
    logger.info(f'My Sounds Prompt: {prompt}')
    return render_template('my_sounds.html', prompt=prompt)

@app.route('/quests')
def quests():
    prompt = prompts.get('Quest', 'Default prompt text')
    logger.info(f'Quests Prompt: {prompt}')
    return render_template('quests.html', prompt=prompt)

def query_chapter_data(chapter):
    query = f"""
    SELECT *
    FROM `vertext-0001.swj_database.data`
    WHERE Chapter = '{chapter}'
    LIMIT 1
    """
    try:
        df = bq_client.query(query).to_dataframe()
        data = df.to_dict(orient='records')
        return data
    except Exception as e:
        logger.error(f"Failed to load care journey data from BigQuery: {e}")
        return None

@app.route('/carejourney/<chapter>')
def carejourney(chapter):
    data = query_chapter_data(chapter)
   
    prompt = prompts.get('Welcome to Your Personalized Care Journey', 'Default prompt text')
    logger.info(f'Care Journey Prompt: {prompt}')
    return render_template('carejourney.html', data=data, prompt=prompt)

@app.route('/my_wellness')
def my_wellness():
    
    prompt = prompts.get('My Wellness', 'Default prompt text')
    logger.info(f'My Wellness Prompt: {prompt}')
    return render_template('my_wellness.html', prompt=prompt)

@app.route('/my_night')
def my_night():
   
    prompt = prompts.get('My Night', 'Default prompt text')
    logger.info(f'My Night Prompt: {prompt}')
    return render_template('my_night.html', prompt=prompt)

@app.route('/breath_rest')
def breath_rest():

    prompt = prompts.get('Breath Rest', 'Default prompt text')
    logger.info(f'Breath Rest Prompt: {prompt}')
    return render_template('breath_rest.html', prompt=prompt)

@app.route('/product_for_me')
def product_for_me():
    
    prompt = prompts.get('Product for Me', 'Default prompt text')
    logger.info(f'Product for Me Prompt: {prompt}')
    return render_template('product_for_me.html', prompt=prompt)

@app.route('/good_night')
def good_night():
    
    prompt = prompts.get('Goodnight', 'Default prompt text')
    logger.info(f'Good Night Prompt: {prompt}')
    return render_template('good_night.html', prompt=prompt)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/annual/<chapter>')
def annual(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Ongoing Support and Annual Follow-Ups', 'Default prompt text')
    logger.info(f'Annual Prompt: {prompt}')
    return render_template('annual.html', data=data, prompt=prompt)

@app.route('/osariskscreening/<chapter>')
def osariskscreening(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('OSA Risk Screening', 'Default prompt text')
    logger.info(f'Osa Prompt: {prompt}')
    return render_template('osariskscreening.html', data=data, prompt=prompt)

    return "Error loading care journey data"

@app.route('/conclusion/<chapter>')
def conclusion(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Conclusion', 'Default prompt text')
    logger.info(f'Conclusion Prompt: {prompt}')
    return render_template('conclusion.html', data=data, prompt=prompt)
  
    return "Error loading care journey data"

@app.route('/smeprovider/<chapter>')
def smeprovider(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Durable Medical Equipment (DME) Provider', 'Default prompt text')
    logger.info(f'(DME) Provider Prompt: {prompt}')
    return render_template('smeprovider.html',data=data, prompt=prompt)

@app.route('/cpap/<chapter>')
def cpap(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('CPAP Therapy', 'Default prompt text')
    logger.info(f'CPAP Therapy Prompt: {prompt}')
    return render_template('cpap.html',data=data, prompt=prompt)

@app.route('/studyresult/<chapter>')
def studyresult(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Positive Sleep Study Results', 'Default prompt text')
    logger.info(f'Study Result Prompt: {prompt}')
    return render_template('studyresult.html',data=data, prompt=prompt)

@app.route('/bookstudy/<chapter>')
def bookstudy(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Scheduling a Sleep Study', 'Default prompt text')
    logger.info(f'Book Study Prompt: {prompt}')
    return render_template('bookstudy.html',data=data, prompt=prompt)

@app.route('/highosarisk/<chapter>')
def highosarisk(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Positive STOP-BANG Results - High Risk for OSA', 'Default prompt text')
    logger.info(f'High Osa Prompt: {prompt}')
    return render_template('highosarisk.html',data = data, prompt=prompt)

@app.route('/doctor/<chapter>')
def doctor(chapter):
    data = query_chapter_data(chapter)
    prompt = prompts.get('Follow-Up Appointment with Your Sleep Doctor', 'Default prompt text')
    logger.info(f'Doctor Prompt: {prompt}')
    return render_template('doctor.html',data=data, prompt=prompt)

@app.route('/startscreen')
def startscreen():
    return render_template('startscreen.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input", "").strip()  # Get user input

    if not user_input:
        return jsonify({"message": "Please provide a valid input."}), 400

    prompt = prompt_template.format(user_input=user_input)
    logger.info(f'Chat Prompt: {prompt}')

    try:
        response = model.generate_content(prompt)
        ai_message = response.text.strip()
        logger.info(f'AI Response: {ai_message}')

        # Process the response to format headings
        formatted_response = ai_message.replace("\n", "<br>")
        return jsonify({"message": formatted_response})

    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        return jsonify({"message": "An error occurred while processing your request."}), 500
@app.route('/voice_to_text', methods=['POST'])
def voice_to_text():
    audio_content = request.files['audio'].read()
    
    client = speech_v1.SpeechClient()
    audio = speech_v1.RecognitionAudio(content=audio_content)
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US"
    )
    
    response = client.recognize(config=config, audio=audio)
    
    text = ""
    for result in response.results:
        text += result.alternatives[0].transcript
    
    return jsonify({"text": text})

@app.route('/text_to_voice', methods=['POST'])
def text_to_voice():
    text = request.json.get("text", "")
if __name__ == '__main__':
    app.run(debug=True)
