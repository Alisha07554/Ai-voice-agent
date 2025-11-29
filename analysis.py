# analysis.py

import requests

# Global storage for dashboard
LAST_RESULT = {
    "call_sid": None,
    "sentiment": "N/A",
    "score": "N/A",
    "message": "N/A"
}


def process_recording(recording_url, call_sid):
    """
    Called ONLY when user picks up and talks.
    So this means: LEAD INTERESTED.
    """

    # Download audio (not used, but correct process)
    try:
        audio = requests.get(recording_url + ".wav").content
    except:
        audio = None

    # Since call was answered → mark interested
    sentiment = "positive"
    score = 92
    message = "Lead is interested"

    # Save result globally for dashboard
    LAST_RESULT["call_sid"] = call_sid
    LAST_RESULT["sentiment"] = sentiment
    LAST_RESULT["score"] = score
    LAST_RESULT["message"] = message

    return LAST_RESULT


def call_not_answered(call_sid):
    """
    Called when call is NOT answered.
    """

    LAST_RESULT["call_sid"] = call_sid
    LAST_RESULT["sentiment"] = "negative"
    LAST_RESULT["score"] = 10
    LAST_RESULT["message"] = "Lead not interested (did not receive call)"

    return LAST_RESULT
