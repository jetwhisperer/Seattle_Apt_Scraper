import re
import datetime


def find_diff_in_xpath(xpath1, xpath2):
    for i in range(min(len(xpath2), len(xpath1))):
        if xpath2[i] != xpath1[i]:
            return xpath1[:i], xpath1[i:], xpath2[i:]


# In a given string, returns the Nth number where n is a typical array index.
def get_nth_number(string: str, n=0):
    p = re.compile(r'(\d*,?\d{1,3})')
    return int(p.findall(string)[n].replace(',', ''))


# Returns the first day available, ignoring the past since we can't tell how long it's been on the market for.
def get_date_available(date_str: str, now_str: str, date_format: str):
    if now_str.lower() in date_str.lower():
        return datetime.datetime.now().date()
    else:
        return datetime.datetime.strptime(date_str, date_format).date()