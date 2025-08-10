from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-gpu")

# Initialize WebDriver
service = Service('chromedriver.exe')  # Update with your path
driver = webdriver.Chrome(service=service, options=chrome_options)

# LinkedIn login credentials
username = " "
password = " "

try:
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Log in to LinkedIn
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(5)  # Wait for login to complete

    # Navigate to the profile page
    driver.get("https://www.linkedin.com/in/your-target-profile/")
    time.sleep(3)

    # Screenshot of the profile page
    profile_screenshot_path = os.path.join(os.getcwd(), 'linkedin_profile.png')
    driver.save_screenshot(profile_screenshot_path)
    print(f"Profile screenshot saved at {profile_screenshot_path}")

    # Example: Extracting the headline from the profile
    headline = driver.find_element(By.CLASS_NAME, "text-heading-xlarge").text
    print(f"Headline: {headline}")

    # Navigate to the "About" section
    about_section = driver.find_element(By.XPATH, "//section[contains(@class, 'pv-about-section')]")
    about_screenshot_path = os.path.join(os.getcwd(), 'linkedin_about.png')
    about_section.screenshot(about_screenshot_path)
    print(f"About section screenshot saved at {about_screenshot_path}")

    # Other data extraction and screenshot logic goes here

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
