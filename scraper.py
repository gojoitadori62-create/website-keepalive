from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sys

def visit_website():
    url = "https://digitvibee.onrender.com/"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        print(f"Starting browser session...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(60)
        
        print(f"Navigating to {url}")
        start_time = datetime.utcnow()
        driver.get(url)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Stay on the page for 1 minute (60 seconds)
        print("Staying on the page for 1 minute...")
        time.sleep(60)
        
        # Take a screenshot for verification
        screenshot_path = f"screenshot_{start_time.strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        
        return {
            'timestamp': start_time.isoformat(),
            'url': url,
            'status': 'success',
            'screenshot': screenshot_path
        }
        
    except Exception as e:
        error_time = datetime.utcnow().isoformat()
        error_msg = str(e)
        print(f"Error: {error_msg}")
        return {
            'timestamp': error_time,
            'url': url,
            'error': error_msg,
            'status': 'error'
        }
        
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()

def log_visit(result):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    status = result['status'].upper()
    if 'error' in result:
        print(f"[{timestamp}] {status} - {result['error']}")
    else:
        duration = (datetime.utcnow() - datetime.fromisoformat(result['timestamp'])).total_seconds()
        print(f"[{timestamp}] {status} - Visited {result['url']} for {int(duration)} seconds")
        if 'screenshot' in result:
            print(f"Screenshot saved as {result['screenshot']}")

if __name__ == "__main__":
    print("Starting website visit...")
    result = visit_website()
    log_visit(result)
    sys.exit(0 if result['status'] == 'success' else 1)
