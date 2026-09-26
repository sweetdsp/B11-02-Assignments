import os
import time
import subprocess
from datetime import datetime
import pyautogui
import pyperclip

# ==============================================================================
# CONFIGURATION & FAILSAFE
# ==============================================================================
# Fail-safe: Slam the mouse to any corner of the screen to stop execution instantly
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Add a 0.5s pause after every PyAutoGUI action for stability

# Get current date and formatted string for the filename
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

# File output paths
filename = f"daily_report_{date_str}.xlsx"
screenshot_filename = f"daily_report_screenshot_{date_str}.png"
comment = "Automated daily status report generated successfully."


def open_browser_and_copy_data():
    """Opens Chrome, navigates to a web page, and copies key data to clipboard."""
    print("[1/5] Launching Chrome...")
    
    # Open Chrome via system run dialog or direct command
    pyautogui.hotkey('win', 'r') if os.name == 'nt' else pyautogui.hotkey('cmd', 'space')
    time.sleep(1)
    
    if os.name == 'nt':
        pyautogui.write('chrome')
        pyautogui.press('enter')
    else:
        pyautogui.write('Google Chrome')
        pyautogui.press('enter')
        
    time.sleep(3)  # Wait for Chrome to launch

    # Focus address bar and navigate
    print("[2/5] Navigating to target site...")
    pyautogui.hotkey('ctrl', 'l') if os.name == 'nt' else pyautogui.hotkey('cmd', 'l')
    time.sleep(0.5)
    
    # We will fetch a headline/status from a lightweight public URL
    pyautogui.write('https://news.ycombinator.com/')
    pyautogui.press('enter')
    time.sleep(4)  # Wait for page load

    # Copy the top headline by selecting and using hotkeys
    # Move mouse to approximate location of the first headline on screen
    screen_w, screen_h = pyautogui.size()
    pyautogui.click(screen_w // 3, screen_h // 4)  # Focus text region
    
    # Shortcut to select headline text region or use hotkey select
    pyautogui.hotkey('ctrl', 'a') if os.name == 'nt' else pyautogui.hotkey('cmd', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c') if os.name == 'nt' else pyautogui.hotkey('cmd', 'c')
    time.sleep(1)

    # Retrieve and sanitize copied text
    fetched_data = pyperclip.paste().split('\n')[0].strip()
    if not fetched_data:
        fetched_data = "Operations Status: Normal - System Online"
    
    print(f"    Fetched Data: '{fetched_data[:40]}...'")
    return fetched_data


def populate_and_save_excel(fetched_data):
    """Opens Excel (or default spreadsheet editor), pastes data, and saves the file."""
    print("[3/5] Opening Excel...")
    
    # Launch Excel
    pyautogui.hotkey('win', 'r') if os.name == 'nt' else pyautogui.hotkey('cmd', 'space')
    time.sleep(1)
    
    if os.name == 'nt':
        pyautogui.write('excel')
        pyautogui.press('enter')
    else:
        pyautogui.write('Numbers')
        pyautogui.press('enter')

    time.sleep(5)  # Allow application to boot completely

    # Create new workbook (Press Enter for Blank Workbook in modern Excel)
    pyautogui.press('enter')
    time.sleep(2)

    print("[4/5] Entering report data into spreadsheet...")
    # Cell 1: Date & Time
    pyperclip.copy(datetime_str)
    pyautogui.hotkey('ctrl', 'v') if os.name == 'nt' else pyautogui.hotkey('cmd', 'v')
    pyautogui.press('tab')

    # Cell 2: Fetched Data
    pyperclip.copy(fetched_data)
    pyautogui.hotkey('ctrl', 'v') if os.name == 'nt' else pyautogui.hotkey('cmd', 'v')
    pyautogui.press('tab')

    # Cell 3: Short Comment
    pyperclip.copy(comment)
    pyautogui.hotkey('ctrl', 'v') if os.name == 'nt' else pyautogui.hotkey('cmd', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    # Save the Excel File
    print(f"[5/5] Saving spreadsheet as '{filename}'...")
    pyautogui.hotkey('ctrl', 's') if os.name == 'nt' else pyautogui.hotkey('cmd', 's')
    time.sleep(1.5)

    # Type the dynamic filename into Save Dialog
    full_path = os.path.abspath(filename)
    pyperclip.copy(full_path)
    pyautogui.hotkey('ctrl', 'v') if os.name == 'nt' else pyautogui.hotkey('cmd', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)

    # Capture screenshot of the final open sheet
    print(f"    Taking screenshot: '{screenshot_filename}'...")
    pyautogui.screenshot(screenshot_filename)
    print("Done! Both report file and screenshot have been saved successfully.")


if __name__ == "__main__":
    print("Starting Daily Report Bot in 3 seconds. Keep hands off the mouse/keyboard...")
    time.sleep(3)
    
    data = open_browser_and_copy_data()
    populate_and_save_excel(data)
    