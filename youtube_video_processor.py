from pytube import YouTube
import os
import tempfile
from audio_video_helpers import extract_audio_from_video, split_large_avfile
from openai_api_helpers import call_to_whisper

    
def youtube_video_handler(url):
    # Create a temporary directory for extracted audio and parts
    with tempfile.TemporaryDirectory() as temp_dir_path:
        #Construct the path for the downloaded video file within the temp directory
        temp_downloaded_video = download_youtube_video(url, temp_dir_path)
        
        # Construct the path for the extracted audio file within the temp directory
        temp_mp3_file_path = os.path.join(temp_dir_path, os.path.basename(url) + "_audio.mp3")
        # Extract audio to the temp file
        extract_audio_from_video(temp_downloaded_video, temp_mp3_file_path)
        
        # Split the audio file if it's larger than the specified max size
        parts= split_large_avfile(temp_mp3_file_path, temp_dir=temp_dir_path)  # Assuming split_large_avfile now only returns the list of parts
        
        combined_transcript = ""
        for part_path in parts:
            transcript = call_to_whisper(part_path)
            combined_transcript += transcript + "\n"
        
        # Return the combined transcript of all parts
        return combined_transcript

def download_youtube_video(url, output_dir):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if video_stream:
            # Construct the output file path
            output_file_path = os.path.join(output_dir, video_stream.default_filename)
            # Download the video
            video_stream.download(output_path=output_dir)
            
            print(f"Downloaded '{video_stream.default_filename}' to '{output_file_path}'")
            
            return output_file_path
        else:
            print("No suitable video stream found.")
            return None
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None