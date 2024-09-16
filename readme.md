# TranscriptToSummary-AI

## Overview
**TranscriptToSummary-AI** is a powerful Streamlit application designed to transform lecture transcripts from Udemy courses into concise summaries and insightful key takeaways. Leveraging the capabilities of Google Generative AI, this application empowers users to easily summarize lengthy content, making learning more efficient and accessible.

## Features
- **API Key Configuration**: Seamlessly enter your Google API key to unlock the summarization features.
- **Flexible Transcript Input**: Choose to paste transcripts directly or upload files in `.txt` or `.srt` formats.
- **Dynamic Summary Generation**: Generate summaries in various lengths—short, medium, or detailed—tailored to your needs.
- **Key Takeaways**: Extract essential points from the transcript to enhance understanding and retention.
- **Question Generation**: Create relevant questions based on the generated summary to test comprehension.
- **Downloadable Summaries**: Easily download your summaries as text files for offline access.

## Requirements
To run the application, ensure you have the following installed:
- Python 3.10 or higher
- Streamlit
- Google Generative AI
- langdetect
- TextBlob
- markdown2
- fpdf

## Installation
Follow these simple steps to get started:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anubhab-m02/TranscriptToSummary-AI
   cd TranscriptToSummary-AI
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Google API key**: 
   - You can either set it in your environment or enter it directly in the app.

## Usage
1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**: 
   Open your web browser and navigate to `http://localhost:8501`.

## How to Use
- **Input Your Transcript**: Choose to paste or upload your transcript.
- **Configure Summary Settings**: Select the desired summary length, number of key takeaways, and language.
- **Generate Summary**: Click the "Generate Summary" button and watch as your transcript is transformed into a concise summary.
- **Download Your Summary**: Enter a file name to download your summary as a text file.
- **Generate Questions**: Use the generated summary to create questions for deeper understanding.

## Contributing
If you have suggestions or improvements, feel free to open an issue or submit a pull request.
