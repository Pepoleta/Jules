from gemini_bot import GeminiBot
import time
import os
import glob

def log(msg):
    with open('flow_log.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg)

# Clear log
with open('flow_log.txt', 'w') as f:
    f.write('')

bot = GeminiBot()
try:
    log("Navigating...")
    bot.navigate_to_gemini()
    
    log("Setting model to Pensar...")
    bot.set_model("Pensar")
    
    # Step 1: Upload ajo.txt
    log("\n--- STEP 1: Upload ajo.txt ---")
    ajo_path = os.path.abspath(os.path.join("tests", "ajo.txt"))
    prompt_1 = "quiero que me ayudes a saber que comer hoy, tengo los ingredientes que te paso en un archivo"
    log("Sending prompt 1...")
    res_1 = bot.send_prompt(prompt_1, [ajo_path])
    log(f"Response 1 length: {len(res_1) if res_1 else 'NONE'}")
    
    # Step 2: Upload zatz files
    log("\n--- STEP 2: Upload zatz files ---")
    zatz_files = glob.glob(os.path.join("tests", "zatz*.txt"))
    zatz_paths = [os.path.abspath(f) for f in zatz_files]
    prompt_2 = "analiza estos archivos y busca mejoras de rendimiento que se puedan aplicar"
    log(f"Sending prompt 2 with {len(zatz_paths)} files...")
    res_2 = bot.send_prompt(prompt_2, zatz_paths)
    log(f"Response 2 length: {len(res_2) if res_2 else 'NONE'}")
    
    log("\nFlow completed successfully.")
except Exception as e:
    log(f"Exception caught: {e}")
finally:
    time.sleep(5)
    bot.close()
