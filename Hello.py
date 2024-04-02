import streamlit as st
from file_helpers import create_user_folders
from uploaded_files_processor import file_upload_handler
from youtube_video_processor import youtube_video_handler
from html_creator import create_html_transcript, create_html_transcript_direclty_gpt4
from pytube import YouTube
import os 

file_name = ''
testing_username = st.secrets['username_test']
def create_download_link(file_name):
    with open(file_name, "r") as file:
        file = file.read()
    st.download_button(label="Download File", data=file, file_name=file_name, mime="text/html")

def set_page_configuration():
    st.set_page_config(
        page_title="AI Accessible HTML Transcripts",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.example.com/help',
            'Report a bug': "https://www.example.com/bug",
            'About': "# This is a transcript creator app using Whisper AI and GPT-4."
        }
    )

def login_user(username, password):
    # This is a placeholder for actual authentication logic
    return username == testing_username and password == "test"

def main():
    set_page_configuration()
    st.header("AI Accessible HTML Transcripts", divider="orange")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    with st.sidebar:
        st.subheader("🦾 User Auth", divider="red")
        with st.container():
            st.markdown("<b>User Authentication</b>", unsafe_allow_html=True)
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                submit = st.button("Login")
            with col2:
                st.empty()
            with col3:
                logout = st.button("Logout")
                
        st.subheader("📁 File Settings", divider="blue")
        with st.container():
            if st.button("Clear Cache", key="clear_cache"):
                with open("file_checker.txt", "w"):
                    pass
        
    if submit:
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
        st.sidebar.success("You're logged out.")
    
    if st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            gpt4_switch = st.toggle("GPT-4", key="gpt4_switch", value=True)
            transcribe_button = st.toggle("Transcribe+", key="transcribe+", value=False)
        with col2:  
            st.empty()
        with col3:
            if st.session_state.user_name is not None:
                st.write(f"Welcome {st.session_state.user_name}")
        
        st.divider()

        uploaded_files = st.file_uploader("Upload a file to transcribe or cleanup", type=['txt', 'mp3', 'vtt', 'mp4'], accept_multiple_files=True)

        with st.container():
            col1, col2= st.columns([2, 1])
            with col1:
                submit_button = st.button("Transcribe", key="transcribe_button")
            with col2:
                st.empty()
            
            
        
        youtube_url = st.chat_input("Paste Youtube Script Here")
        
        if youtube_url:
                with st.status("Processing Youtube Video...", expanded=True) as status:
                    status.write("Starting Download for Youtube Video...")
                    yt = YouTube(youtube_url)
                    raw_text_youtube = youtube_video_handler(youtube_url)
                    status.write("Raw Text Recieved")
                    title = yt.title
                    status.write("Creating a HTML File->Clean up happens here with GPT-4")
                    if transcribe_button is True:
                        youtube_html = create_html_transcript_direclty_gpt4(raw_text_youtube, gpt4_switch)
                    else:
                        youtube_html = create_html_transcript(title, raw_text_youtube, gpt4_switch)
                    status.update(label="File Processed", state="complete", expanded=False)
                    file_path = os.path.join(username, "Transcripts")
                    #save html file in user transcript folder
                    with open(f"{file_path}/{title}.html", "w") as file:
                        file.write(youtube_html)
                        
                with st.container():
                    with st.chat_message(name="assistant", avatar="📁"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"Transcript: {title}")
                        with col2:
                            create_download_link(f"{file_path}/{title}.html") 
              
        if submit_button:
            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    with st.status("Processing File...", expanded=True) as status:
                        status.write("Starting File Processing...")
                        st.write(f"Processing file...{uploaded_file.name}")
                        raw_text_avfile = file_upload_handler(uploaded_file)
                        title = uploaded_file.name
                        st.write(f"Raw Transcript for {title} from Whisper is recieved.")
                        if transcribe_button is True:
                            clean_avfile_html = create_html_transcript_direclty_gpt4(raw_text_avfile, gpt4_switch)
                        else:
                            clean_avfile_html = create_html_transcript(title, raw_text_avfile, gpt4_switch)
                        st.write("File Processed")
                        #create file path for user transcript folder
                        file_path = os.path.join(username, "Transcripts")
                        #save html file in user transcript folder
                        with open(f"{file_path}/{title}.html", "w") as file:
                            file.write(clean_avfile_html)
                        st.write(f"HTML file for {title} is created.")
                    
                    with st.container():
                        with st.chat_message(name="assistant", avatar="📁"):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"Transcript: {title}")
                            with col2:
                                create_download_link(f"{file_path}/{title}.html")    
            else:
                with st.chat_message(name="assistant", avatar="📁"):
                    st.write("No files uploaded yet.")             
    else:
        st.warning("Please login to continue.")

if __name__ == "__main__":
    main()
