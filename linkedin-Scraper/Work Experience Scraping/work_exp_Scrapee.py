from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.linkedin.com/")

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
    try:
        driver.get(link)
        if driver.current_url == "https://www.linkedin.com/404/":
            print("No such profile exists!")
        else:
            extract_info()
    except:
        print("--ERROR--")

def extract_info():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        intro = soup.find('div', {'class': 'pv-text-details__left-panel'}).find("h1")
        name = intro.get_text()
    except:
        print("No profile against this url.")
        return
    experience_section = soup.find("div",{"id": "experience"})
    if experience_section is not None:
        experience = experience_section.parent
        latest_experience = experience.findAll("span",{"class":"t-14"})
        company = latest_experience[0].find("span").get_text().split("·")[0]
        duration = latest_experience[1].find("span").get_text().split("·")[-1]
        [duration := duration.replace(a, b) for a, b in [("mos","month(s)"),("yr","year"),("yrs","year(s)")]]
        print("\nName:\t\'{0}\'\nCompany:\t\'{1}\'\nDuration:\t{2}\n".format(name,company,duration))
    else:
        print("No work-experience found!")


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

