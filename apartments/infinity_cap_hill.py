from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.parse_utils import get_nth_number, get_date_available
from utils.database_utils import add_to_db


class InfinityCapHill:

    @staticmethod
    def name():
        return 'Infinity Capitol Hill'

    @staticmethod
    def run(driver):
        InfinityCapHill.get_infinity_cap_hill(driver)

    # Side note, this property has a `Math.random()` in their apartment URLs. I changed it to a large number and it did nothing special. /shrug
    @staticmethod
    def get_infinity_cap_hill(driver):

        # Bless the devs that give us unique selenium ids
        def get_selenium_id(elem_type, elem_id, base=driver):
            return get_selenium_ids(elem_type, elem_id, base)[0]

        # Base can either be the driver or a parent field
        # // before the xpath will return the global relative xpath. Without will return just the one under the base.
        def get_selenium_ids(elem_type, elem_id, base=driver):
            return base.find_elements_by_xpath(f"{'//' if base is driver else ''}{elem_type}[@data-selenium-id='{elem_id}']")

        driver.get('https://infinitycapitolhillapartments.securecafe.com/onlineleasing/infinity-apartments-0/'
                   'floorplans.aspx')
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((
            By.XPATH, "//div[@data-selenium-id='availability-accordion2']")))

        close_annoying_thing = driver.find_elements_by_class_name('cookieinfo-close')
        if close_annoying_thing:
            close_annoying_thing[0].click()

        apt_floor_elems = []
        try:
            for i in range(1, 100):
                apt_floor_elems.append(get_selenium_id('div', f'availability-accordion{i}'))
                apt_floor_elems[i - 1].click()

        except IndexError:
            pass

        apt_urls = []
        for i, apt in enumerate(apt_floor_elems):
            apt.click()
            try:
                for j in range(1, 200):
                    if get_selenium_id('td', f'Availability_{j}').text == 'CONTACT US':
                        continue
                    availability_elem = get_selenium_id('td', f'Availability_{j}')
                    raw_url_string = availability_elem.find_element_by_xpath('button').get_attribute('onclick')
                    url = f'https://infinitycapitolhillapartments.securecafe.com/onlineleasing/infinity-apartments-0/' \
                          f'availableunits.aspx?myOlePropertyId={get_nth_number(raw_url_string, 0)}&MoveInDate=&t=0' \
                          f'&floorPlans={get_nth_number(raw_url_string, 1)}'
                    apt_urls.append(url)
            except IndexError:
                pass

        for url in apt_urls:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@data-selenium-id='btnUnitSelect1']")))

            # What happened to our lovely selenium IDs, huh?
            model_bed_bath_text = driver.find_element_by_xpath("//div[@id='other-floorplans']").text
            model_string_ind = model_bed_bath_text.find(':') + 2
            apt_model = model_bed_bath_text[model_string_ind: model_string_ind + 2]
            beds = get_nth_number(model_bed_bath_text, 1)
            baths = get_nth_number(model_bed_bath_text, 2)

            try:
                count_floor_plan = len(driver.find_elements_by_class_name('AvailUnitRow'))
                for i in range(1, 200):
                    count_floor_plan -= 1
                    apt_num = get_selenium_id('td', f'Apt{i}').text[1:]
                    sqft = get_nth_number(get_selenium_id('td', f'Sqft{i}').text)
                    rent = get_nth_number(get_selenium_id('td', f'Rent{i}').text)
                    try:
                        special_elem = get_selenium_id('td', f'Specials{i}')
                        special = special_elem.find_element_by_xpath('div/div/div/ul/li/span').get_attribute('innerHTML')
                    except NoSuchElementException:
                        special = ''
                    get_selenium_id('input', f'btnUnitSelect{i}').click()
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//p[@id='MIDateValidationContent']")))
                    available_text = driver.find_element_by_xpath("//p[@id='MIDateValidationContent']").text

                    available = get_date_available(available_text, '', 'Apartment is available for move-in starting on %b/%d/%Y')

                    add_to_db('Infinity Capitol Hill', apt_num=apt_num, bed=beds, bath=baths, sqft=sqft, rent=rent, floor=apt_num[0],
                              available=available, on_special=(special != ''), special_details=special, apt_model=apt_model)
                    if count_floor_plan >= 1:
                        driver.get(url)
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@data-selenium-id='btnUnitSelect1']")))

            except IndexError:
                pass
