import time

from loguru import logger
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

from core import (
    setupWebdriver,
    setupMetamask,
    addNetwork,
    changeNetwork,
)

from config import metamask_secrets, twitter_config

# Load environment variables
load_dotenv()
METAMASK_EXTENSION_URL = (
    "https://github.com/maxafanasiev/metamask-test/blob/main/metamask-chrome-12.7.2.zip"
)


def setup_driver() -> WebDriver:
    # Download and install ChromeDriver

    # metamask_path = downloadMetamask(METAMASK_EXTENSION_URL)
    metamask_path = "extension/metamask-chrome-12.7.2.zip"
    driver = setupWebdriver(
        metamask_path,
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        version="131.0.6778.87",
        chromedriver_path="/opt/homebrew/bin/chromedriver",
    )
    logger.info("Driver setup complete.")
    # Initialize MetaMask with the driver instance
    setupMetamask(metamask_secrets.RECOVERY_PHRASES, metamask_secrets.PASSWORD)
    addNetwork(
        metamask_secrets.NETWORK_NAME,
        metamask_secrets.NETWORK_ENDPOINT,
        metamask_secrets.NETWORK_ID,
        metamask_secrets.NETWORK_SYMBOL,
    )
    changeNetwork(metamask_secrets.NETWORK_NAME)

    return driver


# Step 1: Open Spotlight and connect wallet and Twitter
def connect_wallet_and_twitter(driver):
    driver.get("https://app.spotlightprotocol.com/authenticate")
    time.sleep(2)

    # Connect wallet
    connect_wallet_btn = driver.find_element(
        By.XPATH, "//p[text()='Connect Wallet']/following-sibling::button"
    )
    connect_wallet_btn.click()
    time.sleep(2)

    # Connect metamask
    connect_metamask = driver.find_element(
        By.XPATH,
        "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button",
    )
    connect_metamask.click()
    time.sleep(2)

    # Connect Twitter
    connect_twitter_btn = driver.find_element(
        By.XPATH, "//p[text()='Connect X (Twitter)']/following-sibling::button"
    )

    # Check if the button is not disabled before attempting to click
    if not connect_twitter_btn.get_attribute("disabled"):
        driver.execute_script("arguments[0].scrollIntoView(true);", connect_twitter_btn)
        connect_twitter_btn.click()
        time.sleep(2)

        # Handle Twitter login
        twitter_username_field = driver.find_element(By.NAME, "text")
        twitter_username_field.send_keys(twitter_config.TWITTER_USERNAME)
        twitter_username_field.send_keys(Keys.RETURN)
        time.sleep(2)

        twitter_password_field = driver.find_element(By.NAME, "password")
        twitter_password_field.send_keys(twitter_config.TWITTER_PASSWORD)
        twitter_password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        print("Connected to Twitter")
    else:
        print("Connect Twitter button is disabled. Skipping...")


# Step 2: Mint a Spotlight
def mint_spotlight(driver):
    driver.get("https://app.spotlightprotocol.com/badge")
    time.sleep(2)

    # Locate the "Mint a Spotlight" link
    try:
        mint_spotlight_link = driver.find_element(
            By.XPATH,
            "//p[text()='Mint a Spotlight']/following-sibling::a[contains(@class, 'chakra-button')]",
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", mint_spotlight_link)
        mint_spotlight_link.click()
        time.sleep(2)
        print("Mint a Spotlight action initiated.")
    except Exception as e:
        print(f"Error while trying to mint a Spotlight: {e}")


# Step 3: Join a Spotlight
def join_spotlight(driver):
    driver.get("https://app.spotlightprotocol.com/explore")
    time.sleep(2)

    # Click on a random Spotlight circle
    spotlight_circles = driver.find_elements(
        By.XPATH, "//button[contains(text(), 'Mint Now')]"
    )
    if spotlight_circles:
        spotlight_circles[0].click()
        time.sleep(2)

    print("Joined a Spotlight.")


# Step 4: Mint the Badge
def mint_badge(driver):
    driver.get("https://app.spotlightprotocol.com/badge")
    time.sleep(2)

    claim_btn = driver.find_element(
        By.XPATH, "//button[contains(text(), 'Claim this Badge')]"
    )
    claim_btn.click()
    time.sleep(5)

    print("Badge claimed.")


if __name__ == "__main__":
    driver1 = setup_driver()
    connect_wallet_and_twitter(driver1)
    mint_spotlight(driver1)  # Not working
    join_spotlight(driver1)  # Not working
    mint_badge(driver1)  # Not working
