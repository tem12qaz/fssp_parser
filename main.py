import time

from selenium import webdriver
from bs4 import BeautifulSoup as bs4


def main():
    output = []
    url = 'https://fssp.gov.ru/iss/iP'
    driver = webdriver.Chrome()
    driver.get(url)
    while True:
        resp = driver.page_source
        soup = bs4(resp, 'html.parser')
        result = soup.find('table', class_='list border table alt-p05')
        if result:
            break
        time.sleep(1)
    results = result.find_all('tr')[2:]
    for result in results:
        rows = result.find_all('td')

        if result.find('div', class_='pay-wrap'):
            data = rows[0].get_text(strip=True, separator='|').split('|')
            name = data[0]
            date = data[1]
            place = data[2]

            ip_n = rows[1].get_text(strip=True, separator='|').split('|')[0]

            data = rows[2].get_text(strip=True, separator='|').split('|')
            sp_date, sp_n = data[0].replace('Судебный приказ от ', '').split(' № ')
            sud = data[2]

            sum = rows[4].get_text(strip=True, separator='|').split('|')[1].replace('Исполнительский сбор: ', '')

            fssp_name, fssp_address = rows[5].get_text(strip=True, separator='|').split('|')

            sud_name, phone = rows[6].get_text(strip=True, separator='|').split('|')

            

        return


if __name__ == '__main__':
    main()