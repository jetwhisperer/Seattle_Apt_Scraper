import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.database_utils import add_to_db
from utils.parse_utils import get_nth_number, get_date_available


class Via6:

    @staticmethod
    def name():
        return 'Via6'

    @staticmethod
    def run(driver):
        Via6.get_via6(driver)

    @staticmethod
    def get_via6(driver):
        driver.get('https://via6seattle.com/floorplans/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Interactive Map')))
        tabs = driver.find_elements_by_class_name('skylease__filter-tab-item')
        time.sleep(3)
        for tab in tabs:
            if 'Floor' in tab.text:
                tab.click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'skylease-listing__item')))
        time.sleep(3)
        listings = driver.find_elements_by_class_name('skylease-listing__item')
        for listing in listings:
            availability = listing.find_element_by_class_name('skylease-listing__info--price').text
            if availability[0] == 'C':
                continue

            apt_model = listing.find_element_by_class_name('skylease-listing__title').text
            apt_details = listing.find_element_by_class_name('skylease-listing__info').find_elements_by_xpath('span')
            apt_bed_text = apt_details[0].text
            apt_bed = 0 if apt_bed_text == 'Studio' else get_nth_number(apt_bed_text)
            apt_bath = get_nth_number(apt_details[1].text)
            apt_sqft = get_nth_number(apt_details[2].text)
            listing.click()
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Check Availability')))
            time.sleep(.5)
            driver.find_element_by_partial_link_text('Check Availability').click()
            time.sleep(2)
            rows = driver.find_elements_by_class_name('skylease-unit-table__row')[1::2]
            for row in rows:
                apt_elems = row.find_elements_by_xpath('td')
                apt_num = apt_elems[0].text[1:]
                apt_floor = get_nth_number(apt_elems[1].text, 0)
                apt_rent = get_nth_number(apt_elems[2].text, 0)
                apt_avail_unformatted = apt_elems[4].text
                avail = get_date_available(apt_avail_unformatted, 'Now', 'Available %b %d, %Y')

                add_to_db(complex="Via6", apt_num=apt_num, bed=apt_bed, bath=apt_bath, sqft=apt_sqft, rent=apt_rent,
                          floor=apt_floor, available=avail, apt_model=apt_model)
            driver.find_element_by_class_name('skylease__details-close').click()
