import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class MetamaskConfig:
    RECOVERY_PHRASES: str
    PASSWORD: str
    PERSONAL_KEY: str
    NETWORK_ID = "1088"
    NETWORK_NAME = "MY_MATIC"
    NETWORK_SYMBOL = "Metis"
    NETWORK_ENDPOINT = "https://andromeda.metis.io/?owner=1088"


@dataclass
class TwitterConfig:
    TWITTER_USERNAME: str
    TWITTER_PASSWORD: str


def load_metamask_config() -> MetamaskConfig:
    RECOVERY_PHRASES = os.environ.get("RECOVERY_PHRASES", "")
    PASSWORD = os.environ.get("PASSWORD", "")
    PERSONAL_KEY = os.environ.get("PERSONAL_KEY", "")

    return MetamaskConfig(
        RECOVERY_PHRASES=RECOVERY_PHRASES, PASSWORD=PASSWORD, PERSONAL_KEY=PERSONAL_KEY
    )


def load_twitter_config() -> TwitterConfig:
    TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

    return TwitterConfig(
        TWITTER_USERNAME=TWITTER_USERNAME, TWITTER_PASSWORD=TWITTER_PASSWORD
    )


metamask_secrets: MetamaskConfig = load_metamask_config()
twitter_config: TwitterConfig = load_twitter_config()
