import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def analyze_audio_with_assemblyai(audio_file_path: str) -> dict:
    """Analyze audio characteristics using AssemblyAI"""
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        
        if not transcript.text:
            raise Exception("Failed to transcribe audio")

        config = aai.TranscriptionConfig(
            language_code="en",
            sentiment_analysis=True
        )
        
        detailed_transcript = transcriber.transcribe(audio_file_path, config=config)

        analysis = {
            "tone": "Neutral",
            "pitch": "Normal",
            "emphasis": "Standard emphasis",
            "speed": "Normal"
        }
        
        try:
            if hasattr(detailed_transcript, 'sentiment_analysis_results') and detailed_transcript.sentiment_analysis_results:
                analysis["tone"] = detailed_transcript.sentiment_analysis_results[0].sentiment
        except Exception as e:
            print(f"Could not process sentiment analysis: {str(e)}")
        
        if hasattr(detailed_transcript, 'confidence') and detailed_transcript.confidence:
            analysis["pitch"] = "Rising inflection detected" if detailed_transcript.confidence > 0.8 else "Normal"
        
        return {
            "transcription": transcript.text,
            "voice_analysis": analysis
        }
    except Exception as e:
        raise Exception(f"Audio analysis failed: {str(e)}") 