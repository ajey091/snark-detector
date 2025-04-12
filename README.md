# Snark Detector

A machine learning-powered application that analyzes audio recordings to detect snarkiness in speech. The app uses OpenAI's GPT-4 for text analysis and AssemblyAI for audio transcription and analysis.

## Features

- Audio recording and file upload capabilities
- Real-time transcription of audio content
- Snarkiness detection and scoring
- Detailed analysis of snarky phrases
- Voice characteristics analysis (tone, pitch, emphasis, speed)

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- AssemblyAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ajey091/snark-detector.git
cd snark-detector
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

## Usage

1. Start the application:
```bash
python run.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Choose your input method:
   - Upload an audio file (WAV, MP3, or M4A format)
   - Record audio directly in the browser

4. Wait for the analysis to complete

5. Review the results:
   - Transcription of your audio
   - Overall snark score
   - Specific snarky phrases detected
   - Voice characteristics analysis

## Project Structure

```
snark-detector/
├── src/
│   ├── audio/           # Audio recording and processing
│   ├── analysis/        # Text and audio analysis
│   ├── ui/             # UI components
│   └── app.py          # Main application
├── requirements.txt    # Project dependencies
├── run.py             # Application entry point
└── README.md          # Project documentation
```

## Dependencies

- streamlit==1.41.1
- python-dotenv==0.20.0
- openai==0.25.0
- assemblyai==0.36.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4
- AssemblyAI for audio transcription and analysis
- Streamlit for the web interface 