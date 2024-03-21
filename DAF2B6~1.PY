import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime

element_for_Total_Play_speed = '''
<a class="no-link-chev btnBanner" href="/personaliza?150#internet" promo-name="150 megas 2p" promo-id="1" target="_blank">
    <img class="d-none d-md-block w-100" src="/assetsv2/img/home/sliders/Banner1.png">
    <img class="d-block d-md-none" src="/assetsv2/img/home/sliders/Banner1_mobile.png">
</a>'''

pattern = r'promo-name="(\d+)'  # this is an integer
match = re.search(pattern, element_for_Total_Play_speed)
if match:
    extracted_text = match.group(1)
else:
    extracted_text = "No internet speed found."

PROMISED_SPEEDS_DOWN = extracted_text
PROMISED_SPEEDS_UP = 10
TWITTER_EMAIL = "YOUR_EMAIL"
TWITTER_PASSWORD = "YOUR_PASSWORD"
URL_FOR_SPEEDTEST = "https://www.speedtest.net/"
TWITTER_URL = "https://twitter.com/"

class InternetSpeedTwitterBot:
    def __init__(self, PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP):
        self.driver = self.init_driver()
        self.PROMISED_SPEEDS_DOWN = PROMISED_SPEEDS_DOWN
        self.PROMISED_SPEEDS_UP = PROMISED_SPEEDS_UP
        self.open_website(URL_FOR_SPEEDTEST)

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        self.log_message("webdriver initialized.")
        return driver

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{timestamp} - {message}")

    def open_website(self, url):
        self.driver.get(url)
        self.log_message(f"Successfully opened the website: {url}")
        self.print_test_for_megas_speed(self.PROMISED_SPEEDS_DOWN, self.PROMISED_SPEEDS_UP)
        time.sleep(2)
        self.press_go_button_and_get_internet_speed()

    def print_test_for_megas_speed(self, PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP):
        self.log_message(
            f"The Promised Download speed which is stated on Total Play's Website is: {PROMISED_SPEEDS_DOWN} (Mbps)")
        self.log_message(
            f"The Promised Upload speed which is stated on Total Play's Website is: {PROMISED_SPEEDS_UP} (Mbps)")

    def press_go_button_and_get_internet_speed(self):
        # Implementation goes here, omitted for brevity
        pass

    def tweet_at_provider(self, twitter_email, twitter_password):
        self.log_message("Preparing to tweet at provider.")
        self.login_twitter(twitter_email, twitter_password)

    def login_twitter(driver, email, password):
        start_time = time.time()  # start timing
        driver.get(TWITTER_URL)
        log_message("Twitter page loaded.")

        wait = WebDriverWait(driver, 10)  # reduced wait time to 10 seconds for optimization
        try:
            sign_in_button_xpath = "/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a/div/span/span"
            sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath)))
            sign_in_button.click()
            log_message("Sign-in button clicked.")

            selectors = [
                (By.XPATH, "//input[@name='session[username_or_email]']"),
                (By.CSS_SELECTOR, "input[autocomplete='username']"),
                (By.XPATH,
                 "//*[@id='react-root']/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input"),
                (By.XPATH,
                 "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input")
            ]

            for by, value in selectors:
                try:
                    email_field = wait.until(EC.presence_of_element_located((by, value)))
                    break  # if the field is found, break out of the loop
                except (TimeoutException, NoSuchElementException):
                    log_message(f"Failed to find email field using {by}='{value}'")

            email_field.send_keys(email)
            log_message("Email entered.")

            email_field.send_keys(Keys.RETURN)
            log_message("Email submitted.")

            password_selectors = [
                (By.NAME, 'password'),
                (By.CSS_SELECTOR, 'input[type="password"][autocomplete="current-password"]'),
                (By.CSS_SELECTOR, '.r-30o5oe'),
                (By.XPATH, "//input[@autocomplete='current-password']"),
                (By.XPATH, "//input[@type='password']")
            ]

            password_field = None
            for by, value in password_selectors:
                try:
                    password_field = wait.until(EC.presence_of_element_located((by, value)))
                    if password_field:
                        break
                except (NoSuchElementException, TimeoutException):
                    log_message(f"Password field not found with {by}='{value}'")

            if password_field:
                password_field.send_keys(password)
                log_message("Password entered.")
                password_field.send_keys(Keys.RETURN)
                log_message("Login submitted.")
                end_time = time.time()  # end timing
                total_time = end_time - start_time
                log_message(f"Login completed in {total_time} seconds.")
            else:
                log_message("Failed to find the password field with any method.")

        except Exception as e:
            log_message(f"An error occurred: {str(e)}")


# instantiates and uses the InternetSpeedTwitterBot class
if __name__ == "__main__":
    bot = InternetSpeedTwitterBot(PROMISED_SPEEDS_DOWN, PROMISED_SPEEDS_UP)
    bot.tweet_at_provider(TWITTER_EMAIL, TWITTER_PASSWORD)


def main():
    start_time = time.time()
    driver = init_driver()
    login_twitter(driver, TWITTER_EMAIL, TWITTER_PASSWORD)
    end_time = time.time()
    total_time = end_time - start_time
    # log_message(f"Total time from program start to login: {total_time} seconds.")
    log_message("Browser will remain open until manually closed.")
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    main()