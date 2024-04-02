import tempfile
from openai_api_helpers import call_to_whisper
from duplicate_checker import DuplicateChecker
from audio_video_helpers import extract_audio_from_video, split_large_avfile
import os 

duplicate_checker = DuplicateChecker()

    
def audio_video_handler(file_path):
    # Create a temporary directory for extracted audio and parts
    with tempfile.TemporaryDirectory() as temp_dir_path:
        # Construct the path for the extracted audio file within the temp directory
        temp_mp3_file_path = os.path.join(temp_dir_path, os.path.basename(file_path) + "_audio.mp3")
        
        # Extract audio to the temp file
        extract_audio_from_video(file_path, temp_mp3_file_path)
        
        # Split the audio file if it's larger than the specified max size
        parts= split_large_avfile(temp_mp3_file_path, temp_dir=temp_dir_path)  # Assuming split_large_avfile now only returns the list of parts
        
        combined_transcript = ""
        for part_path in parts:
            transcript = call_to_whisper(part_path)
            combined_transcript += transcript + "\n"
        
        # Return the combined transcript of all parts
        return combined_transcript

def file_upload_handler(uploaded_file):
    file_content = uploaded_file.read()
    print(uploaded_file.type)
    file_hash = duplicate_checker.calculate_file_hash(file_content)
    
    if not duplicate_checker.is_file_processed(file_hash):
        with tempfile.TemporaryDirectory() as temp_dir_path:
            with tempfile.NamedTemporaryFile(delete=True, dir=temp_dir_path) as temp_file:
                temp_file.write(file_content)
                file_path = temp_file.name
                # Check if the uploaded file is an MP4 file
                if uploaded_file.type == "video/mp4":
                    text = audio_video_handler(file_path)
                    if text:
                        duplicate_checker.record_processed_file(file_hash)
                        return text
        

        
        