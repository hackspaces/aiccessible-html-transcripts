import os

def create_user_folders(user_id):
    #get the base path
    base_path = os.path.dirname(os.path.abspath(__file__))
    user_path = os.path.join(base_path, user_id)
    downloads_path = os.path.join(user_path, "Downloads")
    transcripts_path = os.path.join(user_path, "Transcripts")
    
    # Create the directories if they don't exist
    os.makedirs(downloads_path, exist_ok=True)
    os.makedirs(transcripts_path, exist_ok=True)

    return downloads_path, transcripts_path