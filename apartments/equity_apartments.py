import json
import time

from selenium.common.exceptions import NoSuchElementException

from utils.database_utils import add_to_db
from utils.parse_utils import get_nth_number, get_date_available


class EquityApartments:

    @staticmethod
    def name():
        return 'EquityApartments'

    @staticmethod
    def run(driver):
        apts = \
            [('2300 Elliott', 'https://www.equityapartments.com/seattle/belltown/2300-elliott-apartments'),
             ('Alcyone', 'https://www.equityapartments.com/seattle/south-lake-union/alcyone-apartments'),
             ('Cascade', 'https://www.equityapartments.com/seattle/south-lake-union/cascade-apartments'),
             ('Centennial Tower and Court', 'https://www.equityapartments.com/seattle/belltown/centennial-tower-and-court-apartments'),
             ('Bellevue Meadows', 'https://www.equityapartments.com/seattle/redmond/bellevue-meadows-apartments'),
             ('Chloe on Madison', 'https://www.equityapartments.com/seattle/pike-pine/chloe-on-madison-apartments'),
             ('Chloe on Union', 'https://www.equityapartments.com/seattle/pike-pine/chloe-apartments'),
             ('City Square (Bellevue)', 'https://www.equityapartments.com/seattle/downtown-bellevue/city-square-bellevue-apartments'),
             ('Moda', 'https://www.equityapartments.com/seattle/belltown/moda-apartments'),
             ('Olympus', 'https://www.equityapartments.com/seattle/belltown/olympus-apartments'),
             ('Harbor Steps', 'https://www.equityapartments.com/seattle/downtown-seattle/harbor-steps-apartments'),
             ('Harrison Square', 'https://www.equityapartments.com/seattle/uptown/harrison-square-apartments'),
             ('Helios', 'https://www.equityapartments.com/seattle/downtown-seattle/helios-apartments'),
             ('Junction 47', 'https://www.equityapartments.com/seattle/west-seattle/junction-47-apartments'),
             ('Mark on 8th', 'https://www.equityapartments.com/seattle/south-lake-union/mark-on-8th-apartments'),
             ('Metro on First', 'https://www.equityapartments.com/seattle/uptown/metro-on-first-apartments'),
             ('Odin', 'https://www.equityapartments.com/seattle/ballard/odin-apartments'),
             ('Packard Building', 'https://www.equityapartments.com/seattle/capitiol-hill/packard-building-apartments'),
             ('Redmond Court (Bellevue)', 'https://www.equityapartments.com/seattle/redmond/redmond-court-apartments'),
             ('Rianna', 'https://www.equityapartments.com/seattle/capitol-hill/rianna-apartments'),
             ('Saxton', 'https://www.equityapartments.com/seattle/first-hill/saxton-apartments'),
             ('Seventh and James', 'https://www.equityapartments.com/seattle/first-hill/seventh-and-james-apartments'),
             ('Springline (Kinda far)', 'https://www.equityapartments.com/seattle/admiral-district/springline-apartments'),
             ('Square One', 'https://www.equityapartments.com/seattle/roosevelt/square-one-apartments'),
             ('The Heights on Capitol Hill', 'https://www.equityapartments.com/seattle/capitol-hill/the-heights-on-capitol-hill-apartments'),
             ('The Pearl', 'https://www.equityapartments.com/seattle/capitiol-hill/the-pearl-apartments-capitol-hill'),
             ('Three20', 'https://www.equityapartments.com/seattle/capitol-hill/three20-apartments'),
             ('Uwajimaya', 'https://www.equityapartments.com/seattle/international-district/uwajimaya-village-apartments'),
             ('Urbana', 'https://www.equityapartments.com/seattle/ballard/urbana-apartments'),
             ('Venn (Bellevue)', 'https://www.equityapartments.com/seattle/downtown-bellevue/venn-at-main-apartments')]
        for (name, url) in apts:
            try:
                EquityApartments.get_equity_apartments(driver, name, url)
            except Exception as e:
                print(e)

    @staticmethod
    def get_equity_apartments(driver, name, url):
        in_count = 0
        driver.get(url + '##unit-availability-tile')
        time.sleep(3)

        # If there's none of this element, it's _full_
        try:
            total = get_nth_number(driver.find_element_by_class_name('bedroomtype-container.bedroomtype-all').text)
        except NoSuchElementException:
            return
        view_more_buttons = driver.find_elements_by_class_name('panel-footer.more-available')
        for button in view_more_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(0.5)

        units = driver.find_elements_by_class_name('specs')
        for unit in units:
            in_count += 1
            detail = unit.find_element_by_class_name('pricing-container')
            # for detail in details:
            json_details = json.loads(detail.find_element_by_xpath('a').get_attribute('ui-sref')[19:-2])
            apt_num = json_details['UnitId']
            if json_details["Floor"].lower() == 'penthouse' or json_details["Floor"].lower() == 'top floor':
                floor = 99
            elif json_details["Floor"].lower() == 'ground floor':
                floor = 1
            elif json_details["Floor"] == '':
                floor = get_nth_number(apt_num[:-2])
            else:
                floor = get_nth_number(json_details["Floor"])
            rent = int(json_details["BestTerm"]["Price"])
            avail = get_date_available(json_details['AvailableDate'], 'now', '%m/%d/%Y')
            sqft = int(json_details['SqFt'])
            bed = int(json_details['Bed'])
            bath = int(json_details['Bath'])
            floor_plan = json_details['FloorplanName']
            special = json_details['Special']['Active']
            special_details = json_details['Special']['Title']
            special_exp = json_details['Special']['Expires']
            reg_price = 0
            strikethrough = unit.find_element_by_class_name('strikethrough-pricing').get_attribute(
                'ng-show').lower() == 'true'
            if strikethrough:
                reg_price = get_nth_number(unit.find_element_by_class_name('strikethrough-pricing').text)
            on_sale = strikethrough

            add_to_db(name, apt_num=apt_num, bed=bed, bath=bath, sqft=sqft, rent=rent, floor=floor,
                      available=avail, apt_model=floor_plan, on_sale=on_sale, on_special=special,
                      special_details=special_details, sale_expire=special_exp, reg_price=reg_price)
        assert in_count == total
