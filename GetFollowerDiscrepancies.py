from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import PASSWORD

def login(driver):
    print("Logging in...")
    # Wait for the username field to be present
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys(PASSWORD.username)
    
    # Wait for the password field to be present
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(PASSWORD.password)
    
    # Submit the form by sending Enter key to the password field
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(Keys.RETURN)

def click_button_with_css(driver, css_selector):
    print(f"Clicking button with CSS selector: {css_selector}")
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Failed to click button with CSS selector {css_selector}: {e}")
        print("Page source at the time of failure:", driver.page_source)
        raise

def navigate_to_profile(driver):
    print("Navigating to profile...")
    profile_button_css = 'div.x9f619.x1n2onr6.x1lliihq.x1l56gv.x6s0dn4'
    click_button_with_css(driver, profile_button_css)

def navigate_to_followers(driver):
    print("Navigating to followers...")
    followers_css = f'a[href="/{PASSWORD.username}/followers/"]'
    click_button_with_css(driver, followers_css)

def handle_notifications_pop_up(driver):
    try:
        not_now_button_css = 'button._a9--._a9_1'
        print("Checking for notifications pop-up...")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, not_now_button_css))
        ).click()
        print("Clicked 'Not Now' button on notifications pop-up.")
    except Exception as e:
        print("Notifications pop-up not found or failed to click 'Not Now'. Continuing...")
        pass

def __main__():
    print("Starting script...")
    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.instagram.com/accounts/login/')
    
    login(driver)
    
    # Add a small delay to ensure the page is fully loaded
    print("Waiting for 10 seconds before continuing...")
    time.sleep(10)
    
    print("Continuing script...")
    
    # Handle notifications pop-up if present
    handle_notifications_pop_up(driver)
    
    navigate_to_profile(driver)
    time.sleep(3)  # Add a small delay to ensure the profile page loads
    
    navigate_to_followers(driver)
    
    time.sleep(30)  
    driver.quit()  
    print("Script completed successfully.")

__main__()