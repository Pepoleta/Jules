import streamlit as st
import os
import tempfile
from gemini_bot import GeminiBot

st.set_page_config(page_title="Gemini Automator", layout="wide")

# Initialize bot in session state so we don't recreate it on every rerun
if 'bot' not in st.session_state:
    st.session_state.bot = None

def get_bot():
    if st.session_state.bot is None:
        st.session_state.bot = GeminiBot()
        st.session_state.bot.navigate_to_gemini()
    return st.session_state.bot

def main():
    st.title("Gemini Automator 🤖")
    st.markdown("Automate Google Gemini using undetected-chromedriver.")

    # Status indicator
    if st.session_state.bot is None:
        st.warning("Browser is not running. Enter a prompt to start it.")
    else:
        st.success("Browser is running and connected.")

    with st.form("gemini_form"):
        prompt_text = st.text_area("Enter your prompt:", height=150)
        uploaded_files = st.file_uploader("Upload files (PDF, images, etc.)", accept_multiple_files=True)
        
        submit_button = st.form_submit_button("Send to Gemini")

    if submit_button:
        if not prompt_text and not uploaded_files:
            st.error("Please enter a prompt or upload files.")
            return

        with st.spinner("Processing..."):
            bot = get_bot()
            
            file_paths = []
            if uploaded_files:
                # Save uploaded files to a temporary directory
                temp_dir = tempfile.mkdtemp()
                for uploaded_file in uploaded_files:
                    # Sanitize filename to prevent path traversal
                    safe_filename = os.path.basename(uploaded_file.name)
                    file_path = os.path.join(temp_dir, safe_filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(file_path)
            
            st.info("Sending request to Gemini...")
            response = bot.send_prompt(prompt_text, file_paths)
            
            if response:
                st.subheader("Response:")
                st.write(response)
            else:
                st.error("Failed to get a response from Gemini.")

if __name__ == "__main__":
    main()