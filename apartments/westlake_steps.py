from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.database_utils import add_to_db
from utils.parse_utils import get_nth_number, get_date_available


class WestlakeSteps:

    @staticmethod
    def name():
        return 'Westlake Steps'

    @staticmethod
    def run(driver):
        WestlakeSteps.get_westlake_steps(driver)

    @staticmethod
    def get_westlake_steps(driver):
        driver.get('https://www.hollandresidential.com/westlake-steps/availability/floor-plans/')
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'apt-table')))
        time.sleep(5)
        rows = driver.find_elements_by_xpath('/html/body/div[6]/div[2]/div[2]/div[3]/div[2]/table/tbody/tr')
        for row in rows:
            apt_num = row.find_element_by_xpath('td[1]').text
            apt_type = row.find_element_by_xpath('td[2]').text.lower()
            apt_urban = 'urban' in apt_type
            bedrooms = 0 if 'studio' in apt_type else get_nth_number(apt_type, 0)
            bathrooms = int(row.find_element_by_xpath('td[3]').text)
            apt_sqft = int(row.find_element_by_xpath('td[4]').text)
            apt_floor = int(row.find_element_by_xpath('td[5]').text)
            apt_rent = int(row.find_element_by_xpath('td[6]').text[1:])
            apt_avail = row.find_element_by_xpath('td[7]').text
            apt_avail = get_date_available(apt_avail, 'now', '%m/%d/%Y')
            add_to_db(complex='Westlake Steps', apt_num=apt_num, bed=bedrooms, bath=bathrooms, sqft=apt_sqft,
                      floor=apt_floor,
                      rent=apt_rent, available=apt_avail, urban=apt_urban)
