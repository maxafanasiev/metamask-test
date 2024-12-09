import time

from app import SpotlightAutomation


def main():
    try:
        SpotlightAutomation().__call__()
    except Exception:
        SpotlightAutomation().driver.close()
        time.sleep(1)
        main()


if __name__ == "__main__":
    SpotlightAutomation().__call__()