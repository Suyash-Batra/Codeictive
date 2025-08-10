from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from PIL import Image

app = Flask(__name__)

@app.route('/link', methods=['POST'])
def getvalue():
    name= request.form['um']
    password= request.form['p']
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")


    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    def scrollandsave(name):
        c=0
        while(True):
            initial_height=driver.get_window_position()['y']
            str1=name+str(c)+".png"
            c+=1
            profile_screenshot_path = os.path.join(os.getcwd(), str1)
            driver.save_screenshot(profile_screenshot_path)
            time.sleep(2)
            new_height = driver.get_window_position()['y']
            current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            # Check if at the bottom
            if current_scroll_position >= scroll_height:
                print("You've reached the bottom of the page!")
                break
            else:
                print("Still scrolling...")
                driver.execute_script("window.scrollBy(0,1080)")

    def makepdf():
        image_file=[]
        list_ignore=["chat.py","chromedriver.exe","pdfmaker.py","sel.py","trial.py","merged_chats.pdf","__pycache__","deleter.py","hakoton","sh","pass.py","templates","apitry.py"]
        for name in os.listdir(os.getcwd()):
            if name not in list_ignore:
                image_file.append(name)

        # Open the images and convert them to RGB (if they're not already in RGB mode)
        images = [Image.open(img).convert('RGB') for img in image_file]

        # Save the images as a single PDF file
        pdf_filename = "./hakoton/merged_chats.pdf"
        images[0].save(pdf_filename, save_all=True, append_images=images[1:])

    def removess():
        image_file=[]
        list_ignore=["chat.py","chromedriver.exe","pdfmaker.py","sel.py","trial.py","merged_chats.pdf","__pycache__","deleter.py","hakoton","sh","pass.py","templates","apitry.py"]
        for name in os.listdir(os.getcwd()):
            if name not in list_ignore:
                os.remove(name)




    driver.get("https://www.linkedin.com/login")

    driver.set_window_size(1920,1080)  

    input_username = driver.find_element(By.ID,"username")
    input_password = driver.find_element(By.ID,"password")



    input_username.send_keys(name)
    input_password.send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)

    WebDriverWait(driver,40).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id='ember16']"))
    )
    driver.find_element(By.XPATH,"//*[@id='ember16']").click()

    time.sleep(1)

    driver.find_element(By.PARTIAL_LINK_TEXT,"View Profile").click()

    time.sleep(2)

    scrollandsave('linkedin_profile')


    time.sleep(1)

    driver.find_element(By.XPATH,"//*[@id='ember16']").click()

    time.sleep(1)

    driver.find_element(By.PARTIAL_LINK_TEXT,"Posts").click()

    time.sleep(2)

    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/div/section/div[2]/div/div/div/div')))

    # # Get the element's location and size
    # location = element.location
    # size = element.size

    # print(location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height'])
    # # Take a full-page screenshot
    # driver.save_screenshot('full_page_screenshot.png')

    # # Open the full-page screenshot and crop the desired area
    # with Image.open('full_page_screenshot.png') as img:
    #     cropped_img = img.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))
    #     cropped_img.save('element_screenshot.png')


    scrollandsave('linkedin_posts')

    driver.find_element(By.PARTIAL_LINK_TEXT,"Messaging").click()
    time.sleep(1)
    chat_threads = driver.find_elements(By.CLASS_NAME, 'msg-conversation-listitem__link')

    # Iterate over each chat thread, open it, and take a screenshot
    for i,chat in enumerate(chat_threads):
        chat.click()  # Open the chat
        time.sleep(3) 
        str1="Linkedin_chat"+str(i)+".png"
        profile_screenshot_path = os.path.join(os.getcwd(), str1)
        driver.save_screenshot(profile_screenshot_path)
        # screenshot_filename = f'full_chat_screenshot_{i+1}.png'
        # driver.save_screenshot(screenshot_filename)

        # # Locate the chat box to crop (this needs to be adjusted based on the chat box's actual position and size)
        # chat_box = driver.find_element(By.CLASS_NAME, 'msg-s-message-list__event')  # Adjust the class name to match the chat box

        # # Get the location and size of the chat box
        # location = chat_box.location
        # size = chat_box.size
        # left = location['x']
        # top = location['y']
        # right = left + size['width']
        # bottom = top + size['height']

        # # Open the screenshot using Pillow
        # image = Image.open(screenshot_filename)

        # # Crop the image to the chat box area
        # cropped_image = image.crop((left, top, right, bottom))

        # # Save the cropped image
        # cropped_filename = f'cropped_chat_screenshot_{i+1}.png'
        # cropped_image.save(cropped_filename)
    print("Done")
    time.sleep(5)


    driver.quit()

    makepdf()
    removess()


    # os.system("merged_chats.pdf")
    return render_template('download.html')

if __name__ == "__main__":
    app.run(debug=True)  