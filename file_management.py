import streamlit as st
import os 

def list_files_in_folder(folder_path):
    #List file in the folder
    file_list = os.listdir(folder_path)
    pass

def file_manager():
    st.subheader("File Management", divider="blue")