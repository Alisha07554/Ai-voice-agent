import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

# -----------------------------
# 1. Download audio + transcribe
# -----------------------------
def transcribe_audio(audio_url):
    audio_file = requests.get(audio_url + ".wav")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    files = {
        "file": audio_file.content,
        "model": (None, "gpt-4o-mini-tts")
    }

    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers=headers,
        files=files
    )

    try:
        text = response.json().get("text", "")
    except:
        text = ""

    return text


# ---------------------------------
# 2. AI Sentiment + Score + Follow-up
# ---------------------------------
def analyze_text(text):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You analyze calls. Return JSON."},
            {"role": "user", "content": f"Analyze this: {text}"}
        ]
    }

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=data,
        headers=headers
    ).json()

    try:
        reply = res["choices"][0]["message"]["content"]
    except:
        reply = "{}"

    return reply


# ---------------------------------
# 3. Save record to Airtable
# ---------------------------------
def save_to_airtable(transcript, analysis):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "Transcript": transcript,
            "AI Analysis": analysis
        }
    }

    requests.post(url, headers=headers, json=data)


# ---------------------------------
# 4. MAIN PROCESS FUNCTION
# ---------------------------------
def process_recording(audio_url, call_sid):
    transcript = transcribe_audio(audio_url)

    analysis = analyze_text(transcript)

    save_to_airtable(transcript, analysis)

    return {
        "transcript": transcript,
        "analysis": analysis
    }
