import time

from environs import Env
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.selectors import (
    AGREE_METAMASK_PRIVACY_SELECTOR,
    IMPORT_METAMASK_WALLET_SELECTOR,
    NO_THANKS_METAMASK_SELECTOR,
    WORDS_METAMASK_SELECTOR, SUBMIT_METAMASK_PASSWORD_SELECTOR, DONE_METAMASK_SELECTOR, NEXT_BUTTON_METAMASK_SELECTOR,
    CONNECT_WALLET_BUTTON_SELECTOR, CONNECT_METAMASK_BUTTON_SELECTOR, CONNECT_SELECTOR, APPROVE_SELECTOR,
    SIGN_MESSAGE_SELECTOR, SIGH_IN_CONFIRM_SELECTOR, IMPORT_WALLET_SELECTOR, PRIMARY_BTN
)

env = Env()
env.read_env()


class WalletConnect:
    def __init__(self, driver):
        self.driver = driver
        self.password = env("METAMASK_PASSWORD")
        self.creds = env("METAMASK_CREDS").split(" ")

    def switch_window(self, index: int, count: int):
        WebDriverWait(self.driver, 30).until(ec.number_of_windows_to_be(count))
        self.driver.switch_to.window(self.driver.window_handles[index])
        print(f"Switched to window {self.driver.title}")

    def connect(self):
        WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.XPATH, CONNECT_WALLET_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, CONNECT_WALLET_BUTTON_SELECTOR).click()
        WebDriverWait(self.driver, 30).until(
            ec.presence_of_element_located((By.XPATH, CONNECT_METAMASK_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, CONNECT_METAMASK_BUTTON_SELECTOR).click()
        self.switch_window(-1, 4)
        WebDriverWait(self.driver, 30).until(ec.element_to_be_clickable((By.XPATH, CONNECT_SELECTOR)))
        self.driver.find_element(By.XPATH, CONNECT_SELECTOR).click()
        WebDriverWait(self.driver, 30).until(ec.element_to_be_clickable((By.XPATH, APPROVE_SELECTOR)))
        self.driver.find_element(By.XPATH, APPROVE_SELECTOR).click()
        self.switch_window(-2, 3)
        time.sleep(10)
        # WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.XPATH, SIGN_MESSAGE_SELECTOR)))
        self.driver.find_element(By.XPATH, SIGN_MESSAGE_SELECTOR).click()
        print(len(self.driver.window_handles))

        self.switch_window(-1, 4)
        WebDriverWait(self.driver, 30).until(ec.element_to_be_clickable((By.XPATH, SIGH_IN_CONFIRM_SELECTOR)))
        self.driver.find_element(By.XPATH, SIGH_IN_CONFIRM_SELECTOR).click()
        self.switch_window(-2, 3)
        print("Wallet has been connected successfully")
        time.sleep(1)

    def apply_transaction(self):
        time.sleep(5)
        print(len(self.driver.window_handles))
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        self.switch_window(-1, 5)
        time.sleep(5)
        button1 = self.driver.find_element(By.CSS_SELECTOR, PRIMARY_BTN)
        button1.click()
        time.sleep(60)
        print(len(self.driver.window_handles))
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        self.switch_window(-1, 5)
        time.sleep(10)
        button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='confirm-footer-button']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()

        # button2 = WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.CSS_SELECTOR, PRIMARY_BTN)))
        # button2.click()
        time.sleep(36000)

    def setup_metamask_wallet(self):
        time.sleep(10)
        # self.driver.switch_to.window(self.driver.window_handles[1])
        self.switch_window(1, 3)
        # time.sleep(10)
        WebDriverWait(self.driver, 60).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, AGREE_METAMASK_PRIVACY_SELECTOR)))
        self.driver.find_element(By.CSS_SELECTOR, AGREE_METAMASK_PRIVACY_SELECTOR).click()
        self.driver.find_element(By.XPATH, IMPORT_METAMASK_WALLET_SELECTOR).click()
        self.driver.find_element(By.XPATH, NO_THANKS_METAMASK_SELECTOR).click()

        word_inputs = self.driver.find_elements(By.CLASS_NAME, WORDS_METAMASK_SELECTOR)
        for i in range(0, len(self.creds)):
            word_inputs[i].find_element(By.TAG_NAME, "input").send_keys(self.creds[i])

        self.driver.find_element(By.XPATH, IMPORT_WALLET_SELECTOR).click()

        WebDriverWait(self.driver, 30).until(ec.visibility_of_all_elements_located((By.TAG_NAME, 'input')))

        inputs = self.driver.find_elements(By.TAG_NAME, 'input')
        inputs[0].send_keys(self.password)
        inputs[1].send_keys(self.password)
        inputs[2].click()

        self.driver.find_element(By.XPATH, SUBMIT_METAMASK_PASSWORD_SELECTOR).click()
        WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.XPATH, DONE_METAMASK_SELECTOR)))
        self.driver.find_element(By.XPATH, DONE_METAMASK_SELECTOR).click()
        self.driver.find_element(By.XPATH, NEXT_BUTTON_METAMASK_SELECTOR).click()
        self.driver.find_element(By.XPATH, NEXT_BUTTON_METAMASK_SELECTOR).click()
        print("Wallet has been imported successfully")
        time.sleep(5)
