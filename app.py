from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os

from analysis import process_recording

load_dotenv()
app = Flask(__name__)


# ----------------------------------------------------
# 1. MAKE CALL (simple)
# ----------------------------------------------------
@app.route("/call", methods=["GET"])
def make_call():
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    ngrok_url = os.getenv("NGROK_URL")

    call = client.calls.create(
        to=os.getenv("MY_PHONE"),
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        url=ngrok_url + "/voice"
    )

    return {"sid": call.sid, "status": "calling"}


# ----------------------------------------------------
# 2. VOICE FLOW
# ----------------------------------------------------
@app.route("/voice", methods=["POST"])
def voice():
    r = VoiceResponse()
    r.say("Hello! Please speak after the beep.")

    r.record(
        maxLength=5,
        playBeep=True,
        action="/recording"
    )

    return str(r)


# ----------------------------------------------------
# 3. RECORDING — ALWAYS CALLED
# ----------------------------------------------------
@app.route("/recording", methods=["POST"])
def recording():
    call_sid = request.form.get("CallSid")
    recording_url = request.form.get("RecordingUrl")

    # ❗ Twilio sends "" if call was NOT picked
    if recording_url == "" or recording_url is None:
        process_recording(None, call_sid)
    else:
        process_recording(recording_url, call_sid)

    r = VoiceResponse()
    r.say("Thank you.")
    return str(r)


# ----------------------------------------------------
# RUN SERVER
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
