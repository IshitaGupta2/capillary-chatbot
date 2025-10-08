import streamlit as st
from qa import QAChatbot

st.set_page_config(page_title="Capillary Chatbot", layout="wide")
st.title("💬 Capillary Chatbot (Offline Mode)")

# Initialize chatbot
@st.cache_resource(show_spinner="Loading chatbot (first time takes ~1-2 mins)...")
def load_bot():
    return QAChatbot()

bot = load_bot()

# Input field
query = st.text_input("Ask a question about Capillary:", "")

if query:
    with st.spinner("Thinking..."):
        answer, sources = bot.ask(query)

    st.subheader("🧠 Answer")
    st.write(answer)

    st.subheader("📚 Sources")
    for s in sources:
        st.markdown(f"**[{s['title']}]({s['url']})**")
