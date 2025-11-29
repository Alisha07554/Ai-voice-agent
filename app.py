from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os

from analysis import process_recording

# Load variables from .env
load_dotenv()

app = Flask(__name__)

# -----------------------------
# 1️⃣ MAKE AN OUTGOING CALL
# -----------------------------
@app.route("/call", methods=["GET"])
def make_call():

    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    ngrok_url = os.getenv("NGROK_URL")  # THIS IS CORRECT
    my_phone = os.getenv("MY_PHONE")    # +91 number
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not ngrok_url or not my_phone or not twilio_number:
        return {"error": "Missing NGROK_URL or phone numbers in .env"}, 400

    call = client.calls.create(
        to=my_phone,
        from_=twilio_number,
        url=ngrok_url + "/voice"
    )

    return {"status": "calling your number", "sid": call.sid}


# -----------------------------
# 2️⃣ TWILIO CALL INTERACTION
# -----------------------------
@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    
    response.say("Hello! This is your AI assistant. Speak after the beep.")

    response.record(
        maxLength=8,
        playBeep=True,
        action="/recording",
        trim="trim-silence"
    )

    return str(response)


# -----------------------------
# 3️⃣ HANDLE RECORDING
# -----------------------------
@app.route("/recording", methods=["POST"])
def recording():
    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")

    result = process_recording(recording_url, call_sid)
    print("AI Result:", result)

    response = VoiceResponse()
    response.say("Thank you! Your response has been saved.")
    return str(response)


# -----------------------------
# 4️⃣ RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
