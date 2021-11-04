import time

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from openpyxl import workbook, Workbook
from openpyxl import load_workbook


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
    pre_result = result
    results = result.find_all('tr')[2:]

    next_btn = driver.find_element_by_xpath("//*[contains(text(), 'Следующая')]")
    if next_btn:
        next_btn.click()
        # time.sleep(1)
        while True:
            resp = driver.page_source
            soup = bs4(resp, 'html.parser')
            result = soup.find('table', class_='list border table alt-p05')
            if result:
                print(len(str(pre_result)))
                print(len(str(result)))
                if result == pre_result:
                    print('pass')
                    continue
                break
            time.sleep(1)
        results += result.find_all('tr')[2:]

    print(len(results))
    for result in results:
        rows = result.find_all('td')

        if result.find('div', class_='pay-wrap') and "Судебный приказ" in rows[2].text:
            data = rows[0].get_text(strip=True, separator='|').split('|')
            name = data[0]
            date = data[1]
            place = data[2]

            ip_n = rows[1].get_text(strip=True, separator='|').split('|')[0]

            data = rows[2].get_text(strip=True, separator='|').split('|')
            sp_date, sp_n = data[0].replace('Судебный приказ от ', '').split(' № ')
            sud = data[1]

            data = rows[5].get_text(strip=True, separator='|').split('|')[0]
            subject = data.split(': ')[0]
            start = data.find(': ')
            data = data[start+2:]
            end = data.find(' ')
            sum = data[:end]

            fssp_name, fssp_address = rows[6].get_text(strip=True, separator='|').split('|')

            sud_name, phone = rows[7].get_text(strip=True, separator='|').split('|')
            data = (name, date, place, sp_n, sp_date, sud, ip_n, fssp_name, fssp_address, sud_name, sum, subject, phone)
            output.append(data)
            print('x')

    driver.close()

    while True:
        try:
            path = input('Введите путь к файлу ')
            wb = load_workbook(path)
        except Exception as e:
            try:
                wb = Workbook()
            except Exception as e:
                print('Некорректный путь ')
            else:
                break
        else:
            break

    head = ('ФИО',	'Дата рожд.', 'Место рождения', '№СП', 'Дата СП', 'Мировой суд', '№ ИП', 'ФССП Отдел', 'ФССП Адрес', 'ФИО СПИ', 'Сумма долга', 'Вид задолженности', 'Телефон')
    name = input('Введите название листа ')
    wb.create_sheet(name)
    ws = wb[name]
    ws.append(head)
    for row in output:
        ws.append(row)

    wb.save(path)
    wb.close()


if __name__ == '__main__':
    main()