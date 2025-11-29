        ┌────────────────────────┐
        │      User Phone        │
        │   (Receives Call)      │
        └───────────▲────────────┘
                    │
                    │ Voice Call
                    │
        ┌───────────┴────────────┐
        │        Twilio           │
        │ (Call + Recording URL)  │
        └───────────▲────────────┘
                    │ Webhook
                    │
        ┌───────────┴────────────┐
        │        Flask API        │
        │   /voice and /recording │
        └───────────▲────────────┘
                    │
                    │ Process
                    │
        ┌───────────┴────────────┐
        │     analysis.py         │
        │ Sentiment + Score Logic │
        └───────────▲────────────┘
                    │
                    │ Latest result saved
                    │
        ┌───────────┴────────────┐
        │     Streamlit UI        │
        │  Live Dashboard Output  │
        └────────────────────────┘
# objectives 
1. Objectives

The main objectives of the AI Voice Agent project are:

To make automatic phone calls to leads using Twilio

To let the AI listen to the user's voice, record it, and analyze sentiment

To classify leads as “Interested” or “Not Interested” based on call response

To store the latest result and show it on a live dashboard

To help businesses automate lead qualification without human effort

# Features
Features
1. Live AI Voice Calling (Twilio + Ngrok)

System automatically calls a phone number.

Plays an AI message and records user’s voice response.

2. Call Outcome Detection

If user answers → marked Lead Interested

If user does not answer → marked Lead Not Interested

If lead is interested

3. Real-Time Dashboard

View:

Call SID

AI Message

Whether they answered or not

Updates every call automatically.

# Tech Stack
Backend

Python

Flask

Streamlit dashboard

# APIs Used
API	Purpose
Twilio Voice API	Make calls, play message, record audio
OpenAI API	Analyze sentiment, generate summary, follow-ups
Ngrok	Public URL for Twilio to access local serve

# Project Structure
ai-voice-agent/
│
├── app.py               # Main server + Twilio voice + call routing
├── analysis.py          # AI processing (sentiment, scoring, summary)
├── dashboard.py         # Streamlit dashboard (live updates)
├── .env                 # Environment variables (API keys)
├── requirements.txt     # Dependencies
└── README.md            # Documentation

# How to Run the Project

Follow these exact steps.

1. Activate the environment
cd ai-voice-agent
venv\Scripts\activate

2. Run the Flask backend
python app.py


It will start on:

http://127.0.0.1:5000

3. Start Ngrok to expose port 5000
ngrok http 5000


Copy the Forwarding URL:

https://something.ngrok-free.dev


Put it in your .env file under:

NGROK_URL=your-ngrok-url-here

4. Set Twilio Webhook

In Twilio Console → Phone Numbers → Active Number → Voice Webhook:

https://your-ngrok-url/voice


Save.

5. Test call

Open:

http://127.0.0.1:5000/call


It will call your phone.

6. Open Dashboard
streamlit run dashboard.py

# Future Improvements

Replace dummy audio processing with real speech-to-text.

Add Airtable / Firebase for storing all call records.

Add multi-lead auto-dialler system.

Add user authentication so multiple agents can use dashboard.

Add WhatsApp automation for real follow-up messages



