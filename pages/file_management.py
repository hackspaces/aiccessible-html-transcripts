import streamlit as st

def main():
    if st.session_state.get("authenticated") is False:
        st.write("You are not authenticated.")
    
if __name__ == "__main__":
    main()