import base64
import tempfile
import os

RECORDING_JS = """
<script>
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function startRecording() {
    if (isRecording) return;

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();

            reader.onloadend = () => {
                const base64data = reader.result;
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: base64data
                }, "*");
            };

            reader.readAsDataURL(audioBlob);
            document.getElementById('status').textContent = 'Processing audio...';
            document.getElementById('start-button').disabled = true;
        };

        mediaRecorder.start(100);
        isRecording = true;
        document.getElementById('start-button').style.display = 'none';
        document.getElementById('stop-button').style.display = 'inline';
        document.getElementById('status').textContent = 'Recording in progress...';
    } catch (err) {
        console.error('Error accessing microphone:', err);
        document.getElementById('status').textContent = 'Error: Could not access microphone';
    }
}

function stopRecording() {
    if (!isRecording) return;

    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        isRecording = false;
        document.getElementById('start-button').style.display = 'inline';
        document.getElementById('stop-button').style.display = 'none';
    }
}

window.addEventListener('beforeunload', () => {
    if (isRecording) {
        stopRecording();
    }
});
</script>

<div style="text-align: center;">
<button type="button" id="start-button" onclick="startRecording()"
style="padding: 10px 20px; margin: 5px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
Start Recording
</button>
<button type="button" id="stop-button" onclick="stopRecording()"
style="display: none; padding: 10px 20px; margin: 5px; background-color: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">
Stop Recording
</button>
<div id="status" style="margin-top: 10px; font-weight: bold;"></div>
</div>
"""

def process_audio_data(audio_data, is_recorded=False):
    """Process audio data from either upload or recording"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm' if is_recorded else '.wav') as tmp_file:
            if is_recorded:
                try:
                    base64_data = audio_data.split(',')[1] if ',' in audio_data else audio_data
                    audio_bytes = base64.b64decode(base64_data)
                    tmp_file.write(audio_bytes)
                except Exception as e:
                    raise Exception(f"Error processing recorded audio: {str(e)}")
            else:
                tmp_file.write(audio_data)
            return tmp_file.name
    except Exception as e:
        raise Exception(f"An error occurred while processing audio: {str(e)}")

def cleanup_temp_file(file_path):
    """Clean up temporary audio file"""
    if os.path.exists(file_path):
        os.unlink(file_path) 