import time
import requests
from datetime import datetime

def ping_website():
    url = "https://digitvibee.onrender.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"[{datetime.utcnow()}] Pinging {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        print(f"[{datetime.utcnow()}] Success! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"[{datetime.utcnow()}] Error pinging website: {str(e)}")
        return False

def main():
    print("=" * 50)
    print(f"Starting website pinger at {datetime.utcnow()}")
    print("=" * 50)
    
    # Initial ping
    success = ping_website()
    
    # Stay active for 1 minute with periodic pings
    print(f"\n[{datetime.utcnow()}] Staying active for 1 minute...")
    start_time = time.time()
    
    while (time.time() - start_time) < 60:  # 60 seconds = 1 minute
        time.sleep(10)  # Ping every 10 seconds
        if (time.time() - start_time) < 60:  # Don't ping after the time is up
            ping_website()
    
    print("\n" + "=" * 50)
    print(f"Ping session completed at {datetime.utcnow()}")
    print("=" * 50)

if __name__ == "__main__":
    main()
