from gemini_bot import GeminiBot
import time
import os

bot = GeminiBot()
try:
    print("Navigating...")
    bot.navigate_to_gemini()
    
    # Test setting model
    print("Setting model...")
    bot.set_model("Pro")
    time.sleep(2)
    
    # Test file upload
    print("Uploading file...")
    bot._upload_files([os.path.abspath("ajo.txt")])
    time.sleep(5)
    print("Done. Check browser window.")
finally:
    time.sleep(5)
    bot.close()
