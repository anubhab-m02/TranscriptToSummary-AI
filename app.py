import streamlit as st
import google.generativeai as genai

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

def generate_summary(transcript):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Please summarize the following lecture transcript and provide key takeaways:\n\n{transcript}"
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
    
    if st.button("Generate Summary") and transcript:
        with st.spinner("Generating summary..."):
            summary = generate_summary(transcript)
        
        if summary:
            st.subheader("Summary and Key Takeaways")
            st.write(summary)
            
            # Optional: Save summary to file
            if st.button("Save Summary"):
                with open("summary.txt", "w") as f:
                    f.write(summary)
                st.success("Summary saved to summary.txt")
    elif not transcript:
        st.warning("Please enter the transcript to generate a summary.")

if __name__ == "__main__":
    main()
