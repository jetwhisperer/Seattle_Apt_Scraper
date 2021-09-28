from utils.database_utils import add_to_db
from utils.parse_utils import get_nth_number, get_date_available


class Leeward:

    @staticmethod
    def name():
        return 'Leeward'

    @staticmethod
    def run(driver):
        Leeward.get_leeward(driver)

    @staticmethod
    def get_leeward(driver):
        driver.get('https://www.leewardapts.com/Floor-plans.aspx')
        listings = driver.find_elements_by_class_name('unitContainer')
        for listing in listings:
            bed_bath_floor = listing.find_elements_by_xpath('div/ul/li/strong')
            bed = int(bed_bath_floor[0].text)
            bath = int(bed_bath_floor[1].text)
            floor = int(bed_bath_floor[2].text)

            num_sqft_avail = listing.find_elements_by_xpath('div[2]/div')
            apt_num = num_sqft_avail[0].text[5:]
            sqft = get_nth_number(num_sqft_avail[1].text)
            avail_unformatted = num_sqft_avail[2].text
            avail = get_date_available(avail_unformatted, 'NOW', 'Available: %m/%d/%y')

            rent = get_nth_number(listing.find_element_by_xpath('div[3]/div').text)
            add_to_db('Leeward', apt_num=apt_num, bed=bed, bath=bath, sqft=sqft, rent=rent, floor=floor,
                      available=avail)
