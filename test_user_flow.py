from gemini_bot import GeminiBot
import time
import os
import glob
import traceback

def log(msg):
    with open('flow_log.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg)

# Clear log
with open('flow_log.txt', 'w') as f:
    f.write('')

bot = GeminiBot()
try:
    log("=== STARTING TEST FLOW ===")
    log("Navigating...")
    bot.navigate_to_gemini()
    
    # Step 1: Upload ajo.txt with recipe text
    log("\n--- STEP 1: Upload ajo.txt and ask about food ---")
    ajo_path = os.path.abspath(os.path.join("tests", "ajo.txt"))
    log(f"File path: {ajo_path}")
    log(f"File exists: {os.path.exists(ajo_path)}")
    
    prompt_1 = "quiero que me ayudes a saber que comer hoy, tengo los ingredientes que te paso en un archivo"
    log(f"Sending prompt 1 with 1 file...")
    res_1 = bot.send_prompt(prompt_1, [ajo_path])
    log(f"Response 1: {res_1[:200] if res_1 else 'NONE'}")
    
    log("\nWaiting 5s before step 2...")
    time.sleep(5)
    
    # Step 2: Upload ALL zatz files (multiple files in same session)
    log("\n--- STEP 2: Upload zatz files for optimization analysis ---")
    zatz_files = sorted(glob.glob(os.path.join("tests", "zatz*.txt")))
    zatz_paths = [os.path.abspath(f) for f in zatz_files]
    log(f"Found {len(zatz_paths)} zatz files:")
    for p in zatz_paths:
        log(f"  - {os.path.basename(p)} (exists: {os.path.exists(p)})")
    
    prompt_2 = "analiza estos archivos y busca mejoras de rendimiento que se puedan aplicar"
    log(f"Sending prompt 2 with {len(zatz_paths)} files...")
    res_2 = bot.send_prompt(prompt_2, zatz_paths)
    log(f"Response 2: {res_2[:200] if res_2 else 'NONE'}")
    
    log("\n=== FLOW COMPLETED SUCCESSFULLY ===")
except Exception as e:
    log(f"\n=== EXCEPTION: {e} ===")
    log(traceback.format_exc())
finally:
    log("Closing browser in 10s...")
    time.sleep(10)
    bot.close()
    log("Browser closed.")
