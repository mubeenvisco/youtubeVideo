from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import re

def get_chrome_version():
    try:
        # This works for Windows
        cmd = 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        output = subprocess.check_output(cmd, shell=True).decode()
        version = re.search(r"REG_SZ\s+(\d+\.\d+\.\d+)", output).group(1)
        return version
    except:
        return None

def setup_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Add headless option if needed
    chrome_options.add_argument('--headless=new')
    
    # Use a specific Chrome version if available
    chrome_version = get_chrome_version()
    if chrome_version:
        service = Service(ChromeDriverManager(version="114.0.5735.90").install())
    else:
        service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=chrome_options)

if __name__ == "__main__":
    driver = setup_chrome_driver()
    print("ChromeDriver initialized successfully!")
    driver.quit()