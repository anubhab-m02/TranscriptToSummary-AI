import streamlit as st
import google.generativeai as genai
from langdetect import detect
from textblob import TextBlob
import os

# Function to initialize or get the API key
def get_api_key():
    if 'GOOGLE_API_KEY' not in st.session_state:
        st.session_state['GOOGLE_API_KEY'] = ''
    
    api_key = st.text_input("Enter your Google API Key:", value=st.session_state['GOOGLE_API_KEY'], type="password")
    if api_key:
        st.session_state['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=api_key)
        return True
    return False

def extract_transcript(url):
    st.warning("Due to Udemy's content protection, automatic transcript extraction is not possible. Please manually copy and paste the transcript.")
    transcript = st.text_area("Paste the lecture transcript here:", height=300)
    return transcript if transcript else None

def upload_transcript():
    uploaded_file = st.file_uploader("Upload a transcript file (.txt, .srt):", type=["txt", "srt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        return content
    return None

def generate_summary(transcript, length="short", key_takeaways=3):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Please summarize the following lecture transcript in a {length} format and provide {key_takeaways} key takeaways:\n\n{transcript}"
        )
        
        # Check if the response has content
        if response.parts:
            # Join all text parts of the response
            summary = ''.join(part.text for part in response.parts if hasattr(part, 'text'))
            return summary
        else:
            return "No summary generated."
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

def main():
    st.title("Udemy Lecture Summarizer")
    
    if not get_api_key():
        st.warning("Please enter a valid Google API Key to proceed.")
        return

    url = st.text_input("Enter Udemy lecture URL (for reference only):")
    
    transcript = extract_transcript(url)
    if not transcript:
        transcript = upload_transcript()
    
    summary_length = st.selectbox("Select summary length:", ["short", "medium", "long"])
    key_takeaways = st.slider("Number of key takeaways:", 1, 10, 3)
    
    if st.button("Generate Summary") and transcript:
        with st.spinner("Generating summary..."):
            summary = generate_summary(transcript, length=summary_length, key_takeaways=key_takeaways)
        
        if summary:
            st.subheader("Summary and Key Takeaways")
            st.write(summary)
            
    elif not transcript:
        st.warning("Please enter the transcript to generate a summary.")

if __name__ == "__main__":
    main()
