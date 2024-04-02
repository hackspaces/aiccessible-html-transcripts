from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Extract audio from video files 
def extract_audio_from_video(video_file_path, output_audio_path):
    logging.info(f"Extracting audio from video file: {video_file_path}")
    try:
        video = VideoFileClip(video_file_path)
        video.audio.write_audiofile(output_audio_path)
        logging.info(f"Audio extracted to {output_audio_path}")
        return output_audio_path
    except Exception as e:
        logging.error(f"Error occurred while extracting audio: {e}")
        return None
    
# Split large audio-vido files into smaller parts 
def split_large_avfile(file_path, temp_dir, max_size=24.5*1024*1024):  # max_size in bytes
    file_size = os.path.getsize(file_path)
    if file_size <= max_size:
        logging.info(f"No need to split file: {file_path}")
        return [file_path]  # No need to split

    logging.info(f"Splitting file: {file_path}")
    parts = []
    audio = AudioSegment.from_file(file_path)
    duration = len(audio)
    part_duration = duration * (max_size / file_size)
    
    temp_dir = temp_dir
    start = 0
    part_num = 1
    while start < duration:
        end = min(start + part_duration, duration)
        part = audio[start:end]
        part_file_path = os.path.join(temp_dir.name, f"part_{part_num}.mp3")
        part.export(part_file_path, format="mp3")
        parts.append(part_file_path)
        start = end
        part_num += 1
        logging.info(f"Created part {part_num} for file: {file_path}")

    return parts