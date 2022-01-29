import copy
import time

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from openpyxl import workbook, Workbook
from openpyxl import load_workbook
from selenium.webdriver.common.by import By

from google_sheets import add_to_table

js_query = 'return document.documentElement.innerHTML'


def get_base64_captcha(driver, data):
    elem = driver.find_element(By.ID, "region_id_chosen")
    elem.find_element(By.CLASS_NAME, "chosen-search-input").send_keys("Все регионы")
    elem.find_elements(By.CLASS_NAME, "active-result")[-1].click()
    f_name, l_name, parent = data[0].split(' ')
    date = data[1]

    driver.find_element(By.ID, "input01").send_keys(f_name)
    driver.find_element(By.ID, "input02").send_keys(l_name)
    driver.find_element(By.ID, "input05").send_keys(parent)
    driver.find_element(By.ID, "input06").click()
    driver.find_element(By.ID, "input06").send_keys(date)

    driver.find_element(By.ID, "btn-sbm").click()

    while True:
        try:
            captcha = driver.find_element(By.ID, "capchaVisual")
        except:
            time.sleep(0.5)
        else:
            return captcha.get_attribute('src')


def main(driver, captcha):
    output = []

    driver.find_element(By.ID, "captcha-popup-code").send_keys(captcha)
    driver.find_element(By.ID, "captcha-popup-code").click()

    time.sleep(1)

    try:
        captcha = driver.find_element(By.ID, "capchaVisual")
    except:
        pass
    else:
        return captcha.get_attribute('src')

    while True:
        resp = driver.page_source
        soup = bs4(resp, 'html.parser')
        result = soup.find('table', class_='list border table alt-p05')
        if result:
            break

    results = result.find_all('tr')[1:]
    if result.find('tr', class_='region-title') == results[0]:
        results = result.find_all('tr')[1:]

    results_pre = copy.copy(results)

    while True:
        try:
            next_btn = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Следующая')]")
        except Exception:
            break

        if next_btn:
            time.sleep(2)
            next_btn.click()

            while True:
                result = driver.page_source
                soup = bs4(result, 'html.parser')
                result = soup.find('table', class_='list border table alt-p05')
                if result:
                    results_2 = result.find_all('tr')[1:]
                    if result.find('tr', class_='region-title') == results_2[0]:
                        results_2 = result.find_all('tr')[1:]
                    if results_pre[0] == results_2[0]:
                        time.sleep(1)
                        continue
                    break

            results += results_2
            results_pre = copy.copy(results_2)

        else:
            break

    for result in results:
        rows = result.find_all('td')

        if result.find('div', class_='pay-wrap') and "Судебный приказ" in rows[2].text:
            data = rows[0].get_text(strip=True, separator='|').split('|')
            name = data[0]
            try:
                date = data[1]
            except:
                date = ''
            try:
                place = data[2]
            except:
                place = ''

            ip_n = rows[1].get_text(strip=True, separator='|').split('|')[0]

            data = rows[2].get_text(strip=True, separator='|').split('|')
            sp_date, sp_n = data[0].replace('Судебный приказ от ', '').split(' № ')
            sud = data[1] if data[1].upper() == data[1] else data[2]

            data = rows[5].get_text(strip=True, separator='|').split('|')[0]
            subject = data.split(': ')[0]
            start = data.find(': ')
            data = data[start+2:]
            end = data.find(' ')
            sum = data[:end]

            fssp_name, fssp_address = rows[6].get_text(strip=True, separator='|').split('|')

            sud_name, phone = rows[7].get_text(strip=True, separator='|').split('|')
            data = (name, date, sp_n, sp_date, sud, '', '', '', '', '', '', '', ip_n, fssp_name, fssp_address, sud_name, sum, subject)
            output.append(data)

    driver.close()

    head = ['ФИО', 'Дата рожд.', 'Место рождения', '№СП', 'Дата СП', 'Мировой суд', '№ ИП', 'ФССП Отдел', 'ФССП Адрес', 'ФИО СПИ', 'Сумма долга', 'Вид задолженности', 'Телефон']

    # output.insert(0, head)

    # new_output = []
    # for row in output:
    #     new_output.append([])
    #     for col in row:
    #         if values[row.index(col)]:
    #             new_output[output.index(row)].append(col)

    # for i in range(len(head)):
    #     print(i, ' ', head[i])
    # while True:
    #     try:
    #         to_excel = input('Введите номера колонок для добавления в файл (разделив пробелом)\nДля добавления всех колонок введите пустую строку')
    #         if to_excel == '':
    #             break
    #         else:
    #             to_excel = to_excel.split(' ')
    #         new_head = [head[int(x)] for x in to_excel]
    #         new_output = []
    #         for row in output:
    #             new_output.append([row[int(x)] for x in to_excel])
    #
    #         head = new_head
    #         output = new_output
    #     except Exception as e:
    #         print('Неккоректный ввод')
    #     else:
    #         break

    add_to_table(output)
