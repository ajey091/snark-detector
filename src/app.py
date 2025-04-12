import streamlit as st
from src.audio.recorder import process_audio_data, cleanup_temp_file
from src.analysis.text_analyzer import analyze_text_with_gpt
from src.analysis.audio_analyzer import analyze_audio_with_assemblyai
from src.ui.components import display_analysis_results, display_recorder, display_instructions

# Set up the Streamlit page
st.set_page_config(page_title="Snark Detector", layout="wide")
st.title("Snark Detector")

# Initialize session state
if 'recorded_audio' not in st.session_state:
    st.session_state.recorded_audio = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

def process_audio(audio_data, is_recorded=False):
    """Process audio data from either upload or recording"""
    try:
        # Process audio data and get temporary file path
        tmp_file_path = process_audio_data(audio_data, is_recorded)
        
        # Analyze audio
        st.info("Starting audio analysis...")
        audio_analysis = analyze_audio_with_assemblyai(tmp_file_path)
        
        if audio_analysis:
            # Analyze text with GPT
            st.info("Analyzing text for snarkiness...")
            text_analysis = analyze_text_with_gpt(audio_analysis["transcription"])
            
            if text_analysis:
                display_analysis_results(audio_analysis, text_analysis)
            
        # Clean up
        cleanup_temp_file(tmp_file_path)
            
    except Exception as e:
        st.error(f"An error occurred while processing audio: {str(e)}")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Upload Audio", "Record Audio"])

with tab1:
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'm4a'])
    if uploaded_file is not None:
        process_audio(uploaded_file.getvalue(), is_recorded=False)

with tab2:
    st.write("Click the button below to start recording")
    
    # Add the recorder component
    audio_data = display_recorder()
    
    # Create a container for the status/results
    results_container = st.empty()
    
    # Process the audio when new data is received
    if audio_data and isinstance(audio_data, str) and not st.session_state.processing:
        try:
            st.session_state.processing = True
            st.session_state.recorded_audio = audio_data
            with results_container:
                process_audio(st.session_state.recorded_audio, is_recorded=True)
        finally:
            st.session_state.processing = False

# Display instructions
display_instructions()

# Footer
st.markdown("---")
st.caption("Powered by OpenAI GPT-4 and AssemblyAI") 