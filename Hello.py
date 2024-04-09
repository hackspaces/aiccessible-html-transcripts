import streamlit as st
from file_helpers import create_user_folders
from uploaded_files_processor import file_upload_handler
from youtube_video_processor import youtube_video_handler
from html_creator import create_html_transcript, create_html_transcript_direclty_gpt4
from openai_api_helpers import call_to_gpt4_as_accessibiltychecker
from pytube import YouTube
import os 
import re
import logging 
from bs4 import BeautifulSoup

def extract_p_content(html_content):
    """
    Extracts and returns the text content from all <p> tags within the given HTML content.

    Parameters:
    - html_content (str): A string containing HTML content.

    Returns:
    - list of str: A list containing the text content of each <p> tag found.
    """
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <p> tags in the parsed HTML
    p_tags = soup.find_all('p')
    
    # Extract and return the text content from each <p> tag
    return [tag.get_text() for tag in p_tags]

@st.cache_data()
def output_file_paths():
    return []

output_file_paths = output_file_paths()

#Create a logger
logger = logging.getLogger(__name__)

#Set the log level
logger.setLevel(logging.DEBUG)

file_name = ''
testing_username = st.secrets['username_test']

def truncate_before_last_underscore(filename):
    # Find the position of the last underscore
    pos = filename.rfind('_')
    # If an underscore is found, truncate everything before it (including itself)
    if pos != -1:
        return filename[pos+1:]
    else:
        # If no underscore is found, return the original filename
        return filename


def create_download_link(file_name, key):
    with open(file_name, "r") as file:
        file_data = file.read()
    file_name = truncate_before_last_underscore(file_name)
    cleaned_file_name = file_name.split("Transcripts/")[-1]
    st.download_button(label="Download File", data=file_data, file_name=cleaned_file_name, mime="text/html", key=key)
    

def replace_speaker_name(html_content, speaker_name=None):
    """
    Modifies or removes the speaker name in an HTML content string.
    
    If a speaker name is provided, it replaces the placeholder or existing speaker name
    after 'Speaker: ' within an <h2> tag. If no name is provided, it removes the <h2>
    tag that contains 'Speaker: '.
    
    Parameters:
    - html_content (str): The original HTML content.
    - speaker_name (str, optional): The new speaker name to insert. If None, the speaker
      tag is removed. Defaults to None.
    
    Returns:
    - str: The modified HTML content.
    """
    if speaker_name:
        # Pattern to match '<h2>Speaker:</h2>' and variations thereof, to insert the speaker name
        pattern = r'(<h2[^>]*>Speaker:\s*)(</h2>)'
        replacement = r'\1' + speaker_name + r' \2'
    else:
        # Pattern to remove the entire '<h2>Speaker:</h2>' tag if no speaker name is provided
        pattern = r'<h2[^>]*>Speaker:\s*</h2>'
        replacement = ''
    
    modified_html = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)
    return modified_html


def set_page_configuration():
    st.set_page_config(
        page_title="AI Accessible HTML Transcripts",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.example.com/help',
            'Report a bug': "https://www.example.com/bug",
            'About': "# This is a transcript creator app using Whisper AI and GPT-4."
        }
    )

#create a function to save the file in user transcript folder
def save_file_in_user_folder(file_path, file_name, file_content):
    try:
        with open(f"{file_path}/{file_name}.html", "w") as file:
            file.write(file_content)
        return True
    except Exception as e:
        logger.error(f"An error occurred while saving the file in the user transcript folder: {e}")
        return False

def login_user(username, password):
    # This is a placeholder for actual authentication logic
    return username == testing_username and password == "test"

def process_video(youtube_url=None, uploaded_file=None, transcribe_button=False, gpt4_switch=None, username=""):
    """Process a video from YouTube URL or uploaded file and generate a clean HTML transcript."""
    title = ''
    clean_html = ''
    raw_text = ''
    status_label = ''

    # Determine the source and process accordingly
    if youtube_url:
        print("Processing YouTube URL")
        title, raw_text = process_youtube_url(youtube_url)
        print("Title: ", title)
    elif uploaded_file:
        status_label = "File Received"
        print("Processing Uploaded File")
        title, raw_text = process_uploaded_file(uploaded_file)
        print("Title: ", title)

    # Handle raw text processing
    if raw_text:
        print(raw_text[:100])
        print("Raw Text Received")
        if transcribe_button:
            print("Transcribe Button Pressed")
            status_label = "Creating a Clean HTML File using AI -> GPT-4"
            clean_html = create_html_transcript_direclty_gpt4(raw_text, gpt4_switch=transcribe_button)
            print("Clean HTML Created")
        else:
            status_label = "Cleaning Raw Text using GPT-4"
            clean_html = create_html_transcript(title, raw_text, gpt4_switch)

        # Save the HTML file
        print("Saving HTML File")
        user_file_path = os.path.join(username, "Transcripts")
        save_file_in_user_folder(user_file_path, title, clean_html)
        print("HTML File Saved")
        status_label = "File Processed"
    else:
        status_label = "No file uploaded or duplicate file"

    return status_label, title

def process_youtube_url(youtube_url):
    """Process YouTube URL to get title and raw text."""
    yt = YouTube(youtube_url)
    title = yt.title
    raw_text = youtube_video_handler(youtube_url)
    return title, raw_text

def process_uploaded_file(uploaded_file):
    """Process uploaded file to get title and raw text."""
    title = uploaded_file.name
    raw_text = file_upload_handler(uploaded_file)
    return title, raw_text
        
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


st.session_state.toggle = False
st.session_state.output_file_paths = []

with st.sidebar:
    st.subheader("🦾 User Auth", divider="red")
    with st.container():
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            login = st.button("Login")
        with col2:
            st.empty()
        with col3:
            logout = st.button("Logout")
            
    st.subheader("📁 File Settings", divider="blue")
    with st.container():
        if st.button("Clear Cache", key="clear_cache"):
            with open("file_checker.txt", "w"):
                pass

if login:
    if login_user(username, password):
        st.session_state.authenticated = True
        st.session_state.user_name = username
        create_user_folders(username)
        st.sidebar.success("You're logged in.")
    else:
        st.sidebar.error("Invalid username or password.")
        
if logout:
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.toggle = False
    st.sidebar.error("You're logged out.")

if st.session_state.authenticated is False:
    st.info("Please log in to access the app.")

st.header("AI Accessible HTML Transcripts", divider="orange")
if st.session_state.authenticated:
    try:
        tab1, tab2 = st.tabs(["Transcribe", "Manage Files"])
        with tab1:
            # ----------------------------- Main Page -----------------------------
            # ----------------------------- Options -----------------------------
            with st.container():
                st.write("<i>Additional options</i>", unsafe_allow_html=True)
                #Main Page - Configration Options
                maincol1, maincol2 = st.columns([1, 2])
                with maincol1:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        gpt4_switch = st.toggle("GPT-4", key="gpt4_switch", value=True)
                        transcribe_button = st.toggle("Transcribe+", key="transcribe+", value=st.session_state['toggle'])
                    with col2:
                        if gpt4_switch is True:
                            st.write("🟢")
                        else:
                            st.write("🔴")
                        if transcribe_button is True:
                            st.write("🟢")
                        else:
                            st.write("🔴")
                with maincol2:
                    st.empty()
            st.subheader("", divider="orange")


            #File Uploader Button
            with st.form(key="file_uploader", clear_on_submit=True):
                uploaded_files = st.file_uploader("Upload a file to transcribe or cleanup", type=['txt', 'mp3', 'vtt', 'mp4'], accept_multiple_files=True, label_visibility="collapsed")
                with st.container():
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.empty()
                        #Transcribe Button
                        submit_button = st.form_submit_button("Transcribe")
                    with col2:
                        st.empty()
                
            youtube_url = st.chat_input("Paste Youtube Script Here")
            
            if submit_button or youtube_url:
                with st.status("Processing...", expanded=True) as status:
                    processed_files_count = 0
                    
                    if youtube_url:
                        status_label, title = process_video(youtube_url=youtube_url, transcribe_button=transcribe_button, 
                                                            gpt4_switch=gpt4_switch, username=username)
                        status.update(label=f"{status_label} for {title}")
                    
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            status_label, title = process_video(uploaded_file=uploaded_file,
                                                                transcribe_button=transcribe_button, 
                                                                gpt4_switch=gpt4_switch, username=username)
                            if "Processed" in status_label:
                                processed_files_count += 1
                            status.update(label=f"{status_label} for {title}")
                            
                    if processed_files_count == 0:
                        status.update(label="No files processed.", state="error", expanded=False)
                    else:
                        status.update(label=f"All files processed.{processed_files_count} files", state="complete", expanded=False)
            else:
                st.info("Upload a file or paste a YouTube URL to get started.")

            with st.container():
                username = ''
                if st.session_state.authenticated:
                    username = st.session_state.user_name
                    output_file_paths = [{'title': i, 'path': f"{username}/Transcripts/{i}"} for i in os.listdir(f"{username}/Transcripts")]
                    #output_file_paths = [{'title': i, 'path': f"{username}/Transcripts/{i}"} for i in os.listdir(f"{username}/Transcripts")]
                    for file in output_file_paths:
                        with st.chat_message(name="assistant", avatar="📁"):
                            #list files in user transcript folder
                            col1, col2= st.columns([8, 1])
                            with col1:
                                st.write(f"Transcript: {file['title']}")
                            with col2:
                                with st.popover("⚙️"):
                                    speaker_name = st.text_input("Speaker Name", label_visibility="collapsed", placeholder="Enter Speaker Name :", key=f"{file['title']}+speaker_name")
                                    with open(f"{file['path']}", "r") as f:
                                        file_data = f.read()
                                        file_data = replace_speaker_name(file_data, speaker_name)
                                        raw_text = extract_p_content(file_data)
                                    st.download_button(label="Download", data=file_data, file_name=file['title'], mime="text/html")
                                    st.download_button(label="Download Raw Text", data="\n".join(raw_text), file_name=f"{file['title']}_raw_text.txt", mime="text")
                                    delete = st.button("Delete", key=file['title']+file['path'])
                                    if delete:
                                        os.remove(f"{file['path']}")
                                        st.session_state.output_file_paths = [{'title': i, 'path': f"{username}/Transcripts/{i}"} for i in os.listdir(f"{username}/Transcripts")]
                                        st.rerun()
        # ----------------------------- Manage Files Tab -----------------------------
        with tab2:
            file_data = ''
            accessibility_score = ''
            try:
                st.subheader("Manage Files", divider="blue")
                file_selected = st.selectbox("Select a file to manage", options=[i['title'] for i in output_file_paths])
                if file_selected:
                    with open(f"{username}/Transcripts/{file_selected}", "r") as f:
                        file_data = f.read()
                tab2maincol1, tab2maincol2 = st.columns([1, 1])
                with tab2maincol1:
                    t2minicol1, t2minicol2 = st.columns([0.5, 1])
                    with t2minicol1:
                        st.download_button(label="Download", data=file_data, file_name=file_selected, mime="text/html", key=f"{file_selected}+download_manage")
                    with t2minicol2:
                        accessibility_button = st.button("Accessibility Score")
                        if accessibility_button:
                            with st.spinner("Calculating Accessibility Score..."):
                                accessibility_score = call_to_gpt4_as_accessibiltychecker(file_data)
                with tab2maincol2:
                    t2minicol21, t2minicol22 = st.columns([1, 1])
                    with t2minicol21:
                        st.write(f"{accessibility_score}")
                    with t2minicol22:
                        st.empty()  
                def save_file(file_data):
                    with open(f"{username}/Transcripts/{file_selected}", "w") as f:
                        f.write(file_data)
                new_content = st.text_area(value=file_data, label="File Content", height=800, key=None)
            except Exception as e:
                e = str(e)
                st.error(f"No files added yet, {e}")
    except Exception as e:
        st.error(f"Try Again {e}")
    
