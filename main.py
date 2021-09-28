from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from apartments import EquityApartments, InfinityCapHill, Leeward, Via6, WestlakeSteps

debug = False


# Pick your poison. They should work the same. Only test on Firefox though.
def start_firefox_browser():
    options = FirefoxOptions()
    options.headless = not debug
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    return driver


def start_chrome_browser():
    options = ChromeOptions()
    options.headless = not debug
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver


def main():
    with start_firefox_browser() as driver:
        for apt_complex in [Via6, EquityApartments, InfinityCapHill, Leeward, WestlakeSteps]:
            try:
                apt_complex.run(driver)
            except Exception as e:
                print('Exception in', apt_complex.name())
                print(e)


if __name__ == '__main__':
    main()
