from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.selectors import (
    CONNECT_TWITTER_BUTTON_SELECTOR,
    TWITTER_SIGN_IN,
    TWITTER_LOGIN_INPUT_SELECTOR,
    TWITTER_PASSWORD_INPUT_SELECTOR,
    AUTHORIZE_APP_SELECTOR, TWITTER_PHONE_INPUT_SELECTOR
)
from app.wallet import env


class TwitterConnect:
    def __init__(self, driver):
        self.driver = driver
        self.login = env("TWITTER_LOGIN")
        self.password = env("TWITTER_PASSWORD")
        self.username = env("TWITTER_USERNAME")

    def connect(self):
        WebDriverWait(self.driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, CONNECT_TWITTER_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, CONNECT_TWITTER_BUTTON_SELECTOR).click()
        for _ in range(2):
            WebDriverWait(self.driver, 15).until(
                ec.presence_of_element_located((By.XPATH, TWITTER_SIGN_IN)))
            self.driver.find_element(By.XPATH, TWITTER_SIGN_IN).click()

        sleep(5)

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, TWITTER_LOGIN_INPUT_SELECTOR)))
        login = self.driver.find_element(By.XPATH, TWITTER_LOGIN_INPUT_SELECTOR)
        login.send_keys(self.login)
        login.send_keys(Keys.ENTER)

        if self.__detect_unusual_activity():
            sleep(5)
            # WebDriverWait(self.driver, 15).until(
            #     ec.presence_of_element_located((By.XPATH, TWITTER_PHONE_INPUT_SELECTOR)))
            phone = self.driver.find_element(By.XPATH, TWITTER_PHONE_INPUT_SELECTOR)
            phone.send_keys(self.username)
            sleep(1)
            phone.send_keys(Keys.ENTER)

        sleep(5)

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, TWITTER_PASSWORD_INPUT_SELECTOR)))
        password = self.driver.find_element(By.XPATH, TWITTER_PASSWORD_INPUT_SELECTOR)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 15).until(
                ec.presence_of_element_located((By.XPATH, AUTHORIZE_APP_SELECTOR)))
            self.driver.find_element(By.XPATH, AUTHORIZE_APP_SELECTOR).click()
        except Exception:
            pass

    def __detect_unusual_activity(self) -> bool:
        try:
            return bool(
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH, TWITTER_PHONE_INPUT_SELECTOR))
                ))
        except Exception as e:
            print(e)
            return False
