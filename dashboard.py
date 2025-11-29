import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

st.set_page_config(page_title="AI Voice Agent Dashboard", layout="centered")

st.title("📞 AI Voice Agent Dashboard")
st.write("Live sentiment, score, and lead updates")

# Airtable URL
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

# Fetch data
response = requests.get(url, headers=headers)
data = response.json()

# Show records
st.subheader("Lead Records")
for record in data.get("records", []):
    fields = record.get("fields", {})

    st.markdown("---")
    st.write(f"**Name:** {fields.get('name', 'Unknown')}")
    st.write(f"**Sentiment:** {fields.get('sentiment', 'N/A')}")
    st.write(f"**Score:** {fields.get('score', 'N/A')}")
    st.write(f"**Message:** {fields.get('message', 'N/A')}")
