import time
import uuid

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from app.constants import SPOTLIGHT_URL
from app.selectors import LOGIN_BUTTON_SELECTOR, MINT_BUTTON_SELECTOR, INPUT_NAME_SELECTOR, INPUT_DESCRIPTION_SELECTOR, \
    MINT_NOW_SELECTOR
from app.twitter import TwitterConnect
from app.wallet import WalletConnect


class SpotlightAutomation:
    def __init__(self):
        self.driver = self.__get_driver()
        self.__wallet = WalletConnect(self.driver)
        self.__twitter = TwitterConnect(self.driver)

    @staticmethod
    def __get_driver() -> uc.Chrome:
        options = uc.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--load-extension=extension")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return uc.Chrome(options=options)

    def switch_window(self, index: int, count: int):
        WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(count))
        self.driver.switch_to.window(self.driver.window_handles[index])
        print(f"Switched to window {self.driver.title}")

    def __click_login_button(self):
        self.driver.get(SPOTLIGHT_URL)
        time.sleep(5)
        # WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, LOGIN_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, LOGIN_BUTTON_SELECTOR).click()

    def __mint_spotlight(self):
        WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, MINT_BUTTON_SELECTOR)))
        self.driver.find_element(By.XPATH, MINT_BUTTON_SELECTOR).click()
        self.switch_window(-1, 4)
        WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, INPUT_NAME_SELECTOR)))
        self.driver.find_element(By.XPATH, INPUT_NAME_SELECTOR).send_keys(str(uuid.uuid4()))
        WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, INPUT_DESCRIPTION_SELECTOR)))
        self.driver.find_element(By.XPATH, INPUT_DESCRIPTION_SELECTOR).send_keys(str(uuid.uuid4()))
        self.driver.find_element(By.XPATH, MINT_NOW_SELECTOR).click()
        time.sleep(10)

    def __call__(self, *args, **kwargs):
        self.__wallet.setup_metamask_wallet()
        self.__click_login_button()
        self.__wallet.connect()
        if self.driver.current_url != SPOTLIGHT_URL:
            self.__twitter.connect()
        self.__mint_spotlight()
        self.__wallet.apply_transaction()
