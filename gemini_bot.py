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
        driver = uc.Chrome(options=options, version_main=147)
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
            # Find the exact input div
            input_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "rich-textarea div[contenteditable='true']"))
            )
            
            # Using ActionChains to avoid interactability issues
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            
            try:
                actions.move_to_element(input_area).click().pause(0.5).send_keys(text).perform()
            except Exception:
                # Fallback: pure javascript injection if action chains fail
                self.driver.execute_script('''
                    arguments[0].focus();
                    arguments[0].innerText = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                ''', input_area, text)
                
            time.sleep(1)
            
            # Find and click the send button, or press Enter
            try:
                send_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Send'], button[aria-label*='Enviar']"))
                )
                send_button.click()
            except:
                 # fallback to Enter
                 actions.send_keys(Keys.ENTER).perform()
                 
            print("Prompt sent.")
            return self._wait_for_response()

        except Exception as e:
            print(f"Error sending prompt: {e}")
    def set_model(self, model_name):
        print(f"Setting Gemini model to: {model_name}")
        try:
            # Find the model dropdown
            # It usually contains the text of the currently selected model
            dropdown = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Pro') or contains(text(), 'Rápido') or contains(text(), 'Pensar')]]"))
            )
            current_model = dropdown.text
            if model_name.lower() not in current_model.lower():
                dropdown.click()
                time.sleep(1)
                
                # Click the option
                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{model_name}')]/.."))
                )
                option.click()
                print(f"Model {model_name} selected.")
                time.sleep(3) # Wait for model switch to complete
            else:
                print("Model already selected.")
        except Exception as e:
            print(f"Error setting model or model dropdown not found: {e}")

    def _upload_files(self, file_paths):
        print(f"Attempting to upload {len(file_paths)} files using native OS automation...")
        try:
            import pyautogui
            
            # Formateamos la ruta (en windows se pueden pegar las multiples rutas separadas por espacios y entre comillas)
            if len(file_paths) > 1:
                file_paths_str = " ".join([f'"{p}"' for p in file_paths])
            else:
                file_paths_str = file_paths[0]
            
            # Click the '+' button
            try:
                add_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Herramientas'], button[aria-label*='Tools'], button[aria-label*='Abrir'], button[aria-label*='upload']"))
                )
                add_btn.click()
                time.sleep(1)
            except Exception as e:
                print(f"Could not click '+' button: {e}")
                return
                
            # Click "Subir archivos" asynchronously to avoid blocking Selenium thread with OS dialog
            try:
                upload_menu = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Subir') or contains(text(), 'Upload')]"))
                )
                self.driver.execute_script("var elem = arguments[0]; setTimeout(function() { elem.click(); }, 100);", upload_menu)
            except Exception as e:
                print(f"Could not click 'Subir archivos' menu: {e}")
                return
                
            time.sleep(2.0) # Wait for the native Windows file dialog to open
            
            # Use clipboard to avoid keyboard layout issues with quotes and special characters
            import pyperclip
            pyperclip.copy(file_paths_str)
            time.sleep(0.5)
            
            # Paste the file path using native OS keyboard
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            
            print("Files injected via native dialog using clipboard.")
            time.sleep(5) # Wait for Gemini to process the attachment chip
            
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