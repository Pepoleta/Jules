import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

class GeminiBot:
    def __init__(self, profile_dir="chrome_profile"):
        self.profile_dir = os.path.abspath(profile_dir)
        self.driver = self._init_driver()

    def _init_driver(self):
        options = uc.ChromeOptions()
        # Use a persistent user data directory for Google login session
        options.add_argument(f"--user-data-dir={self.profile_dir}")
        options.add_argument("--profile-directory=Default")
        
        # Initialize the driver
        driver = uc.Chrome(options=options)
        return driver

    def navigate_to_gemini(self):
        print("Navigating to Gemini...")
        self.driver.get("https://gemini.google.com/app")
        
        # We check for the presence of the main chat input area as a sign of being logged in.
        try:
            print("Waiting for chat input area to be visible (sign of successful login)...")
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "rich-textarea"))
            )
            print("Successfully loaded Gemini chat interface.")
        except Exception as e:
            print(f"Timeout waiting for Gemini chat interface. Are you logged in? Error: {e}")
            raise

    def send_prompt(self, text, file_paths=None):
        if file_paths:
            self._upload_files(file_paths)
            time.sleep(2) # Give some time for files to attach

        try:
            # Find the input area
            input_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "rich-textarea"))
            )
            
            # Type the text. We use send_keys.
            input_area.send_keys(text)
            time.sleep(1)
            
            # Find and click the send button, or press Enter
            try:
                send_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Send']"))
                )
                send_button.click()
            except:
                 # fallback to Enter
                 input_area.send_keys(Keys.ENTER)
                 
            print("Prompt sent.")
            return self._wait_for_response()

        except Exception as e:
            print(f"Error sending prompt: {e}")
            return None

    def _upload_files(self, file_paths):
        print(f"Attempting to upload {len(file_paths)} files...")
        try:
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            file_paths_str = "\n".join(file_paths)
            file_input.send_keys(file_paths_str)
            print("Files uploaded.")
            
        except Exception as e:
             print(f"Error uploading files: {e}")

    def _wait_for_response(self):
        print("Waiting for response...")
        try:
            time.sleep(5)
            time.sleep(10) # Wait for generation to finish
            
            responses = self.driver.find_elements(By.CSS_SELECTOR, "message-content")
            if responses:
                last_response = responses[-1]
                return last_response.text
            else:
                return "Could not find response text."
                
        except Exception as e:
             print(f"Error waiting for response: {e}")
             return None

    def close(self):
        if self.driver:
            self.driver.quit()