from selenium import webdriver
import time
from getpass import getpass

class Instabot:

    def __init__(self,user,pasw):

        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument("--incognito")
        #self.chromeOptions.add_argument("--headless")

        self.driver = webdriver.Chrome('./driver/chromedriver.exe', options = self.chromeOptions)
        self.driver.get('https://www.instagram.com/')

        time.sleep(2)

        usrname = self.driver.find_element_by_name("username")
        usrname.send_keys(user)

        pwd = self.driver.find_element_by_name("password")
        pwd.send_keys(pasw)

        loginButton = self.driver.find_element_by_xpath('//div[4]//button[1]')
        loginButton.click()

        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()  #click not now
        self.driver.find_element_by_xpath('//div[@class="Fifk5"]//img[@class="_6q-tv"]').click()  #go to profile


    def goToFollowing(self):
        self.driver.find_element_by_xpath('//main[contains(@class,"o64aR")]//li[3]//a[1]').click()  # following

    def goToFollowers(self):
        self.driver.find_element_by_xpath('//main[contains(@class,"o64aR")]//li[2]//a[1]').click()  # followers

    def getNames(self):
        scrollBox = self.driver.find_element_by_class_name("isgrP")

        lastHt ,ht = 0,1
        while lastHt != ht:                                                    # for scrolling
            lastHt = ht
            time.sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollBox)

        nameLinks = scrollBox.find_elements_by_tag_name("a")
        Names = [name.text for name in nameLinks if name.text != '']

        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()

        return Names


    def writeToFile(self,nameList):
        file = open("namelist.txt", "w")

        i = 1
        for nm in nameList:
            file.write(str(i))
            file.write("      ")
            file.write(nm)
            file.write("\n")
            i = i + 1

        print("CHECK THE FILE FOR LIST")

    def logout(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button').click()
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()


username = input("   Enter Username/Email/Number:::")
password = getpass("   Enter Password:::")

print("\n****PLEASE WAIT****\n")

myBot = Instabot(username,password)
time.sleep(3)

myBot.goToFollowing()
time.sleep(3)
followingNames = myBot.getNames()

time.sleep(2)
myBot.goToFollowers()
time.sleep(3)
followersName = myBot.getNames()

differenceNames = [user for user in followingNames if user not in followersName]
myBot.writeToFile(differenceNames)

myBot.logout()
time.sleep(5)
myBot.driver.close()

ex = input("Press Close to quit")
