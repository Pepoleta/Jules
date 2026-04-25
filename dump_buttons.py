import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time, os

options = uc.ChromeOptions()
options.add_argument(f'--user-data-dir={os.path.abspath("chrome_profile")}')
options.add_argument('--profile-directory=Default')
options.add_argument('--remote-debugging-port=9222')
driver = uc.Chrome(options=options, version_main=147)
driver.get('https://gemini.google.com/app')

print('Waiting for chat input...')
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'rich-textarea')))
print('Chat loaded.')
time.sleep(3)

# Dump all buttons in the INITIAL state
print('\n=== INITIAL STATE BUTTONS ===')
buttons = driver.find_elements(By.TAG_NAME, 'button')
for b in buttons:
    try:
        aria = b.get_attribute('aria-label') or ''
        classes = b.get_attribute('class') or ''
        text = b.text.strip()[:50] if b.text else ''
        displayed = b.is_displayed()
        if (aria or text) and displayed:
            print(f'BTN: aria="{aria}" class="{classes[:100]}" text="{text}"')
    except:
        pass

# Now send a message to change the UI state
print('\n=== SENDING FIRST MESSAGE ===')
input_area = driver.find_element(By.CSS_SELECTOR, "rich-textarea div[contenteditable='true']")
actions = ActionChains(driver)
actions.move_to_element(input_area).click().pause(0.5).send_keys("Hola, como estas?").perform()
time.sleep(1)

send_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Send'], button[aria-label*='Enviar']"))
)
send_button.click()
print('Message sent. Waiting for response...')
time.sleep(15)

# Dump all buttons in the POST-MESSAGE state
print('\n=== POST-MESSAGE STATE BUTTONS ===')
buttons = driver.find_elements(By.TAG_NAME, 'button')
for b in buttons:
    try:
        aria = b.get_attribute('aria-label') or ''
        classes = b.get_attribute('class') or ''
        text = b.text.strip()[:50] if b.text else ''
        displayed = b.is_displayed()
        if (aria or text) and displayed:
            print(f'BTN: aria="{aria}" class="{classes[:100]}" text="{text}"')
    except:
        pass

print('\n=== DONE ===')
# Keep alive for inspection
time.sleep(120)
driver.quit()
