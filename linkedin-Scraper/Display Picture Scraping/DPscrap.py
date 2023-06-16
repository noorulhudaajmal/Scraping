from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import requests


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.linkedin.com/")

if not (os.path.exists(os.path.join(os.getcwd(), "Images"))):
    os.mkdir(os.path.join(os.getcwd(), "Images"))
    os.chdir(os.path.join(os.getcwd(), "Images"))

def get_credentials():
    print("Enter your linkedin login credentials:")
    username = input(">>USERNAME : ")
    password = input(">>PASSWORD : ")
    return username,password

def login_to_linkedin():
    user , pswd = get_credentials()
    username = driver.find_element(by= "id" ,value = 'session_key')
    password = driver.find_element(by= "id" ,value = 'session_password')
    log_in_button = driver.find_element(by = By.CLASS_NAME , value='sign-in-form__submit-button')
    username.clear();password.clear()
    username.send_keys(user)
    password.send_keys(pswd)

    log_in_button.click()
    if driver.current_url == "https://www.linkedin.com/":
        print("Some problem with login credentials")
        return -1
    return 0


def get_profile(link):
    driver.get(link)
    print("get link")
    if driver.current_url == "https://www.linkedin.com/404/":
        print("No such profile exists!")
    else:
        extract_info()


def extract_info():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        intro = soup.find('div', {'class': 'pv-text-details__left-panel'}).find("h1")
        name = intro.get_text()
    except:
        print("No profile against this url.")
        return
    dp = soup.findAll("img",{"class":"ember-view"})[1]["src"]
    print(dp)
    with open(str(name) + '.jpeg', 'wb') as f:
        im = requests.get(dp)
        f.write(im.content)
    print('DOWNLOADING IMG #' + str(dp) + ".jpg")
    print("--------------------------------------")

print("LINKEDIN PROFILE SCRAPING")

while True:
    response = login_to_linkedin()
    if response == 0:
        break

print("Enter -1 to end.")
while True:
    link = input("Profile-url>> ")
    if link.upper()=="-1":
        break
    else:
        get_profile(link)

driver.quit()
print("End!")
