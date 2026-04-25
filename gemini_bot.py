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
            # Find the model dropdown using exact aria-label from DOM inspection
            dropdown = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Abrir selector de modo']"))
            )
            current_model = dropdown.text.strip()
            print(f"  Current model text: '{current_model}'")
            if model_name.lower() not in current_model.lower():
                dropdown.click()
                time.sleep(1.5)
                
                # Click the option in the dropdown menu
                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{model_name}')]"))
                )
                option.click()
                print(f"  Model switched to {model_name}.")
                time.sleep(3)  # Wait for model switch to complete
            else:
                print(f"  Model '{model_name}' already selected.")
        except Exception as e:
            print(f"  Error setting model: {e}")

    def _upload_files(self, file_paths):
        print(f"Attempting to upload {len(file_paths)} files using native OS automation...")
        import pyautogui
        import pyperclip
        
        for i, fpath in enumerate(file_paths):
            print(f"  Uploading file {i+1}/{len(file_paths)}: {os.path.basename(fpath)}")
            try:
                # Click the '+' button (the upload button, NOT the 'Herramientas'/Tools button)
                try:
                    add_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 
                            "button[aria-label='Abrir el menú para subir archivos']"))
                    )
                    add_btn.click()
                    time.sleep(1.5)
                except Exception as e:
                    print(f"  Could not click '+' button: {e}")
                    return
                    
                # Click "Subir archivos" menu item - use async click to avoid blocking on OS dialog
                try:
                    upload_menu = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,
                            "button[role='menuitem'][aria-label*='Subir archivos']"))
                    )
                    self.driver.execute_script(
                        "var elem = arguments[0]; setTimeout(function() { elem.click(); }, 100);", 
                        upload_menu)
                except Exception as e:
                    print(f"  Could not click 'Subir archivos' menu: {e}")
                    # Try pressing Escape to close the menu before returning
                    pyautogui.press('escape')
                    time.sleep(0.5)
                    return
                    
                time.sleep(2.5)  # Wait for the native Windows file dialog to open
                
                # Use clipboard to paste the full file path
                pyperclip.copy(fpath)
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                pyautogui.press('enter')
                
                print(f"  File {i+1} sent to dialog.")
                
                # Wait for Gemini to process the attachment chip before uploading the next one
                time.sleep(4)
                
            except Exception as e:
                print(f"  Error uploading file {i+1}: {e}")
        
        print(f"All {len(file_paths)} file(s) upload process completed.")
        time.sleep(2)  # Extra wait for all chips to settle

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