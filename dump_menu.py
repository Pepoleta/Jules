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
driver = uc.Chrome(options=options, version_main=147)
driver.get('https://gemini.google.com/app')

print('Waiting for chat input...')
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'rich-textarea')))
print('Chat loaded.')
time.sleep(3)

# Send a first message to get to post-message state
print('Sending first message...')
input_area = driver.find_element(By.CSS_SELECTOR, "rich-textarea div[contenteditable='true']")
actions = ActionChains(driver)
actions.move_to_element(input_area).click().pause(0.5).send_keys("Hola").perform()
time.sleep(1)
send_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Send'], button[aria-label*='Enviar']"))
)
send_button.click()
print('Message sent. Waiting for response...')
time.sleep(15)

# Now click the + button and inspect the menu
print('\n=== Clicking + button ===')
add_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Abrir el menú para subir archivos']"))
)
add_btn.click()
time.sleep(2)

# Dump all visible elements that might be the menu items
print('\n=== MENU ITEMS (all visible elements with text) ===')
# Check for menu items, mat-menu-item, etc
for tag in ['button', 'a', 'div', 'span', 'li', 'mat-option']:
    elements = driver.find_elements(By.TAG_NAME, tag)
    for el in elements:
        try:
            if el.is_displayed():
                text = el.text.strip()
                classes = el.get_attribute('class') or ''
                role = el.get_attribute('role') or ''
                aria = el.get_attribute('aria-label') or ''
                if text and ('menu' in classes.lower() or 'item' in classes.lower() or 'option' in classes.lower() 
                    or role in ['menuitem', 'option', 'button'] or 'subir' in text.lower() or 'upload' in text.lower()
                    or 'archivo' in text.lower() or 'file' in text.lower() or 'google' in text.lower()
                    or 'drive' in text.lower() or 'foto' in text.lower()):
                    print(f'  TAG={tag} text="{text[:60]}" class="{classes[:80]}" role="{role}" aria="{aria}"')
        except:
            pass

# Also try a broader search
print('\n=== ALL VISIBLE TEXT-BEARING ELEMENTS ===')
all_els = driver.find_elements(By.XPATH, "//*[text()]")
for el in all_els:
    try:
        if el.is_displayed():
            text = el.text.strip()
            if text and len(text) < 60 and text not in ['', 'Hola']:
                tag = el.tag_name
                classes = (el.get_attribute('class') or '')[:60]
                print(f'  <{tag}> "{text}" class="{classes}"')
    except:
        pass

print('\n=== DONE ===')
time.sleep(5)
driver.quit()
