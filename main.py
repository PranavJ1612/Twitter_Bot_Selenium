import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
SPEEDTEST_URL = "https://www.speedtest.net/"
TWITTER_LOGIN_URL = "https://twitter.com/login"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(SPEEDTEST_URL)
        time.sleep(5)

        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()

        time.sleep(60)
        self.down = float(self.driver.find_element(By.CLASS_NAME, value="download-speed").text)
        self.up = float(self.driver.find_element(By.CLASS_NAME, value="upload-speed").text)
        print(f"Download Speed:{self.down}, Upload Speed:{self.up}")

    def tweet_at_provider(self):
        # STEP 1: LOGIN TO TWITTER ACCOUNT
        self.driver.get(TWITTER_LOGIN_URL)
        time.sleep(3)

        email = self.driver.find_element(By.NAME, "text")
        email.send_keys(TWITTER_EMAIL, Keys.ENTER)
        time.sleep(3)

        username = self.driver.find_element(By.NAME, "text")
        username.send_keys(TWITTER_USERNAME, Keys.ENTER)
        time.sleep(3)

        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(TWITTER_PASSWORD, Keys.ENTER)
        # LOGIN BUTTON XPATH '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button'
        time.sleep(10)

        # STEP 2: MAKE A TWEET ON INTERNET SPEED NOT AS PROMISED
        tweet_compose = self.driver.find_element(By.XPATH,
                                                 value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')

        tweet = (f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for "
                 f"{PROMISED_DOWN}down/{PROMISED_UP}up?")
        tweet_compose.send_keys(tweet)
        time.sleep(5)

        post_button = self.driver.find_element(By.XPATH,
                                               value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
        post_button.click()

        time.sleep(5)
        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
