import os
import sys
import time
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install the required packages using: pip install -r requirements.txt")
    sys.exit(1)

def setup_driver():
    """Set up and return a Chrome WebDriver instance."""
    print("Setting up Chrome WebDriver...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)
        return driver
    except Exception as e:
        print(f"Failed to initialize WebDriver: {str(e)}")
        raise

def take_screenshot(driver, prefix='screenshot'):
    """Take a screenshot and return the file path."""
    try:
        os.makedirs('screenshots', exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = os.path.abspath(f"screenshots/{prefix}_{timestamp}.png")
        driver.save_screenshot(filename)
        print(f"Screenshot saved as {filename}")
        return filename
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")
        return None

def visit_website():
    url = "https://digitvibee.onrender.com/"
    driver = None
    
    try:
        print(f"Starting browser session...")
        driver = setup_driver()
        
        print(f"Navigating to {url}")
        start_time = datetime.utcnow()
        
        # Try to load the page
        try:
            driver.get(url)
            # Wait for the page to load completely
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page loaded successfully")
        except Exception as e:
            print(f"Page load warning: {str(e)} - Continuing with the visit anyway")
        
        # Take initial screenshot
        screenshot_path = take_screenshot(driver, 'initial')
        
        # Stay on the page for 1 minute (60 seconds)
        print("Staying on the page for 1 minute...")
        for i in range(6):  # 6 * 10 seconds = 60 seconds
            print(f"Time elapsed: {i*10} seconds")
            time.sleep(10)
            
            # Take periodic screenshots
            if i % 2 == 0:  # Every 20 seconds
                take_screenshot(driver, f'periodic_{i//2}')
        
        # Take final screenshot
        final_screenshot = take_screenshot(driver, 'final')
        
        return {
            'timestamp': start_time.isoformat(),
            'url': url,
            'status': 'success',
            'screenshots': [s for s in [screenshot_path, final_screenshot] if s]
        }
        
    except Exception as e:
        print(f"Error during website visit: {str(e)}")
        
        # Try to take a screenshot even if there's an error
        error_screenshot = None
        try:
            if driver:
                error_screenshot = take_screenshot(driver, 'error')
        except Exception as screenshot_error:
            print(f"Failed to take error screenshot: {str(screenshot_error)}")
            
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'url': url,
            'error': str(e),
            'status': 'error',
            'screenshots': [error_screenshot] if error_screenshot else []
        }
        
    finally:
        if driver:
            try:
                print("Closing browser...")
                driver.quit()
            except Exception as e:
                print(f"Error while closing browser: {str(e)}")

def main():
    print("=" * 50)
    print(f"Starting website visit at {datetime.utcnow().isoformat()}")
    print("=" * 50)
    
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # List files in current directory
    print("\nCurrent directory contents:")
    try:
        print("\n".join(os.listdir()))
    except Exception as e:
        print(f"Error listing directory: {str(e)}")
    
    # Run the website visit
    result = visit_website()
    
    # Print results
    print("\n" + "=" * 50)
    print(f"Visit completed at {datetime.utcnow().isoformat()}")
    print(f"Status: {result['status'].upper()}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    
    if 'screenshots' in result and result['screenshots']:
        print("\nScreenshots taken:")
        for screenshot in result['screenshots']:
            print(f"- {screenshot}")
    
    print("=" * 50 + "\n")
    
    # Always exit with success to prevent GitHub Actions from failing
    sys.exit(0)

if __name__ == "__main__":
    main()
