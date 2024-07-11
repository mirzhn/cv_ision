from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import json

def load_config(config_path: str) -> dict:
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def setup_driver(driver_path: str, lang: str = "en-US") -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument(f"--lang={lang}")
    return webdriver.Chrome(service=Service(driver_path), options=chrome_options) 

def login_linkedin(driver: webdriver.Chrome, username: str, password: str) -> None:
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password, Keys.RETURN)
    time.sleep(5)   

def save_profile_page(driver: webdriver.Chrome, profile_url: str, output_file: str) -> None:
    driver.get(profile_url)
    time.sleep(5)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

def main():
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    
    config = load_config(CONFIG_PATH)

    if not os.path.exists(config['driver_path']):
        raise FileNotFoundError(f"Driver not found at {config['driver_path']}")
    try:
        driver = setup_driver(config['driver_path'], config['language'])
        try:
            login_linkedin(driver, config['username'], config['password'])
            save_profile_page(driver, config['profile_url'], config['output_file'])
        finally:
            driver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()