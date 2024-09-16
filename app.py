import streamlit as st
import google.generativeai as genai
import time
import base64
import pandas as pd
import streamlit.components.v1 as components


# Set page configuration
st.set_page_config(page_title="Transcript to Summary AI", page_icon="📚", layout="wide")

# Initialize session state variables
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'answers' not in st.session_state:
    st.session_state.answers = None
if 'show_question_gen' not in st.session_state:
    st.session_state.show_question_gen = False

# Function to initialize or get the API key
def get_api_key():
    if 'GOOGLE_API_KEY' not in st.session_state:
        st.session_state['GOOGLE_API_KEY'] = ''
    
    api_key = st.sidebar.text_input("Enter your Google API Key:", value=st.session_state['GOOGLE_API_KEY'], type="password")
    if api_key:
        st.session_state['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=api_key)
        return True
    return False

def extract_transcript():
    transcript_source = st.radio("Choose transcript source:", ["Paste", "Upload"])
    
    if transcript_source == "Paste":
        st.info("Due to Udemy's content protection, automatic transcript extraction is not possible. Please manually copy and paste the transcript.")
        transcript = st.text_area("Paste the lecture transcript here:", height=200)
    else:
        uploaded_file = st.file_uploader("Upload a transcript file (.txt, .srt)", type=["txt", "srt"])
        if uploaded_file is not None:
            transcript = uploaded_file.read().decode("utf-8")
        else:
            transcript = None
    
    return transcript

def generate_content(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if response.parts:
            return ''.join(part.text for part in response.parts if hasattr(part, 'text'))
        else:
            return "No content generated."
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

def generate_summary(transcript, length, key_takeaways, language, user_interests, summary_style):
    interests_prompt = f" Focus on aspects related to {user_interests}." if user_interests else ""
    style_prompt = f" in {summary_style} style" if summary_style else ""
    prompt = f"Please provide a {length} summary of the following lecture transcript and provide {key_takeaways} key takeaways in {language}.{interests_prompt}{style_prompt}\n\n{transcript}"
    return generate_content(prompt)

def generate_questions(summary, num_questions, difficulty, language, question_type, include_answers):
    answer_prompt = " with answers" if include_answers else " without providing answers"
    prompt = f"Based on the following summary, generate {num_questions} {difficulty}-level {question_type} questions in {language}{answer_prompt}:\n\n{summary}"
    return generate_content(prompt)

def save_summary_to_file(summary, file_name):
    b64 = base64.b64encode(summary.encode('utf-8')).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{file_name}.txt" class="btn btn-primary" style="text-decoration:none; color:white; padding:10px 20px; background-color:#4CAF50; border-radius:5px; display:inline-block; text-align:center; width:100%;">📥 Download Summary (TXT)</a>'
    return href

def simulate_progress():
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)

def main():
    st.sidebar.title("📚 Transcript to Summary AI")
    
    if not get_api_key():
        st.sidebar.warning("Please enter a valid Google API Key to proceed.")
        return

    # Sidebar options
    st.sidebar.subheader("Settings")
    default_language = st.sidebar.selectbox("Default Language:", ["English", "Spanish", "French", "German", "Chinese"])
    default_summary_length = st.sidebar.select_slider("Default Summary Length:", ["very short", "short", "medium", "detailed", "very detailed"])
    
    # Main content
    st.title("Transcript to Summary AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("📝 Transcript Input", expanded=True):
            st.session_state.transcript = extract_transcript()

    if st.session_state.transcript:
        with col2:
            with st.expander("🔧 Summary Settings", expanded=True):
                summary_length = st.select_slider("Summary length:", ["very short", "short", "medium", "detailed", "very detailed"], value=default_summary_length)
                key_takeaways = st.slider("Number of key takeaways:", 1, 10, 3)
                language = st.selectbox("Summary language:", ["English", "Spanish", "French", "German", "Chinese"], index=["English", "Spanish", "French", "German", "Chinese"].index(default_language))
                user_interests = st.text_input("Enter your interests or context for personalized summary (optional):")
                summary_style = st.selectbox("Summary style:", ["Paragraph", "Bullet Points"])

        if st.button("🚀 Generate Summary", key="generate_summary_button"):
            with st.spinner("Generating summary..."):
                simulate_progress()
                st.session_state.summary = generate_summary(st.session_state.transcript, summary_length, key_takeaways, language, user_interests, summary_style)
                st.session_state.show_question_gen = True
            
    if st.session_state.summary:
        st.markdown("## 📊 Summary")
        st.write(st.session_state.summary)
        
        st.markdown("### Download Summary")
        file_name = st.text_input("Enter file name for download:", "summary")
        if file_name:
            download_link = save_summary_to_file(st.session_state.summary, file_name)
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.info("Enter a file name to enable download.")

        if st.session_state.show_question_gen:
            st.markdown("## ❓ Question Generation")
            with st.expander("Generate Questions", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    num_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=5, step=1)
                    question_type = st.selectbox("Question type:", ["Multiple Choice", "Short Answer", "True/False"])

                with col2:
                    difficulty = st.selectbox("Question difficulty:", ["Easy", "Medium", "Hard"])
                include_answers = st.checkbox("Include answers in the questions")

                if st.button("🧠 Generate Questions", key="generate_questions_button", use_container_width=True):
                    with st.spinner("Generating questions..."):
                        st.session_state.questions = generate_questions(st.session_state.summary, num_questions, difficulty, language, question_type, include_answers)
                    
    if st.session_state.questions:
        st.markdown("## Generated Questions")
        st.write(st.session_state.questions)
        
    if not st.session_state.transcript:
        st.warning("Please enter or upload a transcript to generate a summary or questions.")

if __name__ == "__main__":
    main()
