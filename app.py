# app.py

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os

from analysis import process_recording, call_not_answered

load_dotenv()
app = Flask(__name__)


# -------------------------------------------------------
# 1️⃣ MAKE OUTGOING CALL
# -------------------------------------------------------
@app.route("/call", methods=["GET"])
def make_call():

    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    my_phone = os.getenv("MY_PHONE")
    ngrok_url = os.getenv("NGROK_URL")

    call = client.calls.create(
        to=my_phone,
        from_=twilio_number,
        url=ngrok_url + "/voice",
        status_callback=ngrok_url + "/status",
        status_callback_event=["completed"],
        status_callback_method="POST"
    )

    return {"status": "calling", "sid": call.sid}


# -------------------------------------------------------
# 2️⃣ TWILIO CALL FLOW
# -------------------------------------------------------
@app.route("/voice", methods=["POST"])
def voice():

    response = VoiceResponse()
    response.say("Hello! This is your AI assistant. Speak after the beep.")

    response.record(
        playBeep=True,
        maxLength=6,
        action="/recording"
    )

    return str(response)


# -------------------------------------------------------
# 3️⃣ DETECT MISSED CALL
# -------------------------------------------------------
@app.route("/status", methods=["POST"])
def call_status():
    call_status = request.form.get("CallStatus")
    call_sid = request.form.get("CallSid")

    if call_status in ["no-answer", "busy", "failed"]:
        call_not_answered(call_sid)

    return "OK", 200


# -------------------------------------------------------
# 4️⃣ RECORDING RECEIVED → LEAD INTERESTED
# -------------------------------------------------------
@app.route("/recording", methods=["POST"])
def recording():

    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")

    process_recording(recording_url, call_sid)

    response = VoiceResponse()
    response.say("Thank you! Your response has been saved.")
    return str(response)


# -------------------------------------------------------
# 5️⃣ RUN SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
