import copy
import time
import traceback

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
#from openpyxl import workbook, Workbook
#from openpyxl import load_workbook
from selenium.webdriver.common.by import By

from google_sheets import add_to_table

from pyvirtualdisplay import Display


js_query = 'return document.documentElement.innerHTML'
driver = ''


def captcha_wrapper(data):
    global driver
    global display
    try:
        captcha = get_base64_captcha((data['fio'], data['date']))
    except:
        print(traceback.format_exc())
        driver.quit()
        display.stop()
        return 'false'
    return captcha


def get_base64_captcha(data):
    print('start')
    global driver
    global display
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--no sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    #path = './'
    #options.add_argument("user-data-dir=" + path)
    #options.add_argument("--disable-gpu")
    #options.add_argument('--remote-debugging-port=9222')
    #options.add_argument("--disable-blink-features")
    #options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument("start-maximized")
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #options.add_experimental_option("prefs", prefs)
    url = 'https://fssp.gov.ru/iss/iP'
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)
    elem = driver.find_element(By.ID, "region_id_chosen")
    elem.find_element(By.CLASS_NAME, "chosen-search-input").send_keys("Все регионы")
    elem.find_elements(By.CLASS_NAME, "active-result")[-1].click()
    f_name, l_name, parent = data[0].replace("\t", '').split(' ')
    date = data[1]
    print(f_name, l_name, parent)

    driver.find_element(By.ID, "input01").send_keys(f_name)
    driver.find_element(By.ID, "input02").send_keys(l_name)
    driver.find_element(By.ID, "input05").send_keys(parent)
    #driver.find_element(By.ID, "input06").click()
    time.sleep(1)
    driver.find_element(By.ID, "input06").send_keys(date)

    driver.find_element(By.ID, "btn-sbm").click()

    while True:
        try:
            print('wait')
            driver.save_screenshot('test.png')
            captcha = driver.find_element(By.ID, "capchaVisual")
        except:
            time.sleep(0.5)
        else:
            return captcha.get_attribute('src')


def main_wrapper(captcha):
    global driver
    global display
    try:
        captcha = main(captcha)
    except Exception as e:
        print(e)
        import traceback
        print(traceback.format_exc())
    else:
        if captcha:
            print('captcha')
            return captcha
    driver.quit()
    display.stop()
    return 'true'


def main(captcha):
    print('--')
    global driver
    output = []
    print(captcha)
    driver.find_element(By.ID, "captcha-popup-code").send_keys(captcha)
    driver.find_element(By.ID, "ncapcha-submit").click()

    time.sleep(3)

    try:
        #driver.find_element(By.ID, "captcha-popup-code")
        captcha = driver.find_element(By.ID, "capchaVisual")
        loader = driver.find_element(By.CLASS_NAME, "b-center-loader")
        if captcha and loader:
            raise ZeroDivisionError
        #print(captcha)
    except:
        pass
    else:
        print('src')
        return captcha.get_attribute('src')

    i = 0
    while True:
        resp = driver.page_source
        soup = bs4(resp, 'html.parser')
        result = soup.find('table', class_='list border table alt-p05')
        print('--')
        i += 1
        time.sleep(1)
        if i == 10:
            return 'empty'
        if result:
            #driver.save_screenshot('test.png')
            break

    results = result.find_all('tr')[1:]
    if result.find('tr', class_='region-title') == results[0]:
        results = result.find_all('tr')[1:]

    results_pre = copy.copy(results)
    #driver.save_screenshot('test.png')
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
            data = (name.title(), date, sp_n, sp_date, sud, '', '', '', '', '', '', '', ip_n, fssp_name, fssp_address, sud_name.title(), sum, subject)
            output.append(data)
    #driver.quit()
    #driver.close()
    #display.stop()
    #driver.save_screenshot('test.png')  
    print(output)
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
    print('quit')
