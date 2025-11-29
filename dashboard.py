# dashboard.py

import streamlit as st
from analysis import LAST_RESULT

st.title("📞 AI Voice Agent Dashboard")

st.subheader("Latest Call Details")

st.write(f"**Call SID:** {LAST_RESULT.get('call_sid')}")
st.write(f"**Sentiment:** {LAST_RESULT.get('sentiment')}")
st.write(f"**Score:** {LAST_RESULT.get('score')}")
st.write(f"**Message:** {LAST_RESULT.get('message')}")

st.info("Refresh the page after each call to see updates.")
