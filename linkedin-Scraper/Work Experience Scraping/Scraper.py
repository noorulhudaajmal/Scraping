from linkedin_api import Linkedin
from datetime import datetime


class Scraper:

    USER_NAME = "your-user-name"
    PASSWORD = "your-password"

    def __init__(self):
        self.setup_api(self.USER_NAME,self.PASSWORD)
        while self.api==-1:
            usr,pas = self.get_credentials()
            self.setup_api(usr,pas)
        #-----LINKED-API NOW HAS BEEN SETUP AGAINST YOUR ACCOUNT TO SCRAP THE WEBSITE-----
        self.process_scraping()


    def get_credentials(self):
        print("Your LinkedIn credentials (2FA must be disabled)")
        username = input("username/email : ")
        password = input("password : ")
        return username,password


    def setup_api(self,user,pas):
        try:
            self.api = Linkedin(user,pas)
        except:
            print("Invalid credentials")
            self.api = -1

    def get_public_profile_info(self):
        choice = input("Would You like to search profile by\n1.profile username\n2.profile url\n>>[1 or 2]>>")
        if choice=="1":
            user = input("\n username: ")
            print("\n")
        elif choice=="2":
            userUrl = input("\n profile-url: ")
            print("\n")
            if len(userUrl.split("/")[-1])!=0:
                user = userUrl.split("/")[-1]
            else:
                user = userUrl.split("/")[-2]
        else:
            print("Invalid choice!")
            return -1
        result = self.api.get_profile(user)
        if len(result)!=0:
            return result
        else:
            print("No such profile exists!")
            return -1

    def extract_experience(self,info_dict):
        name = info_dict["firstName"] + " "+info_dict["lastName"]
        if "experience" in info_dict.keys():
            experience = info_dict["experience"]
            if len(experience)!=0:
                latest_experience = experience[0]
                company = latest_experience["companyName"]
                start = latest_experience["timePeriod"]["startDate"]
                if "endDate" in latest_experience["timePeriod"].keys():
                    end = latest_experience["timePeriod"]["endDate"]
                    days = (datetime(day=1,month=end["month"],year=end["year"]) - datetime(day=1,month=start["month"],year=start["year"])).days
                else:
                    days = (datetime.now() - datetime(day=1,month=start["month"],year=start["year"])).days
                years = days//365
                months = (days-years*365)//30
                print("\'{0}\' working at \'{1}\' for {2} year(s) and {3} month(s).".format(name,company,years,months))
            else:
                print("No work experience available for this user!")
        else:
            print("User-Profile Error!")

    def process_scraping(self):
        while True:
            info_dict = self.get_public_profile_info()
            if info_dict!=-1:
                self.extract_experience(info_dict)
            print("\n")
            cont = input("Would you like to search for another user?[Y,N]",)
            if cont.upper() == "Y":
                print("----------------------------------------------------------")
                pass
            else:
                break

scrapee = Scraper()
