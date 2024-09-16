# TranscriptToSummary-AI
## Overview
The TranscriptToSummary-AI is a Streamlit application that allows users to summarize lecture transcripts from Udemy courses. Users can either paste the transcript directly or upload a transcript file. The application utilizes Google Generative AI to generate concise summaries and key takeaways from the provided content.

## Features
- **API Key Configuration**: Users can enter their Google API key to enable the summarization feature.
- **Transcript Input**: Users can paste the transcript directly or upload a `.txt` or `.srt` file.
- **Summary Generation**: The application generates summaries in short, medium, or long formats, along with key takeaways.

## Requirements
- Python 3.10 or higher
- Streamlit
- Google Generative AI
- langdetect
- TextBlob

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/anubhab-m02/TranscriptToSummary-AI
   cd TranscriptToSummary-AI
   ```

2. Install the required packages:
   ```bash
   pip install streamlit google-generativeai langdetect textblob
   ```

3. Set your Google API key in the environment or enter it in the app.

## Usage
1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

