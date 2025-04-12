import streamlit as st
from src.audio.recorder import RECORDING_JS

def display_analysis_results(audio_analysis, text_analysis):
    """Display the analysis results in the UI"""
    # Display transcription
    st.subheader("Transcription")
    st.write(audio_analysis["transcription"])
    
    # Display snark score
    st.subheader("Snark Score")
    st.progress(text_analysis["score"] / 100)
    st.write(f"{text_analysis['score']}/100")
    
    # Display detected phrases
    st.subheader("Detected Snarky Phrases")
    if text_analysis["phrases"]:
        for phrase in text_analysis["phrases"]:
            st.write(f'**"{phrase["phrase"]}"** (Score: {phrase["score"]}/10)')
            st.write(f'Context: {phrase["context"]}')
            st.write("---")
    else:
        st.write("No snarky phrases detected!")
    
    # Display voice analysis
    st.subheader("Voice Analysis")
    col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
    with col1:
        st.metric("Tone", audio_analysis["voice_analysis"]["tone"])
    with col2:
        st.metric("Pitch", audio_analysis["voice_analysis"]["pitch"])
    with col3:
        st.metric("Emphasis", audio_analysis["voice_analysis"]["emphasis"])
    with col4:
        st.metric("Speed", audio_analysis["voice_analysis"]["speed"])

def display_recorder():
    """Display the audio recorder component"""
    return st.components.v1.html(
        RECORDING_JS,
        height=150
    )

def display_instructions():
    """Display usage instructions"""
    with st.expander("How to use"):
        st.write("""
        1. Choose either:
           - Upload an audio file (WAV, MP3, or M4A format)
           - Record audio directly in the browser
        2. Wait for the analysis to complete
        3. Review the results:
           - Transcription of your audio
           - Overall snark score
           - Specific snarky phrases detected
           - Voice characteristics analysis
        """) 