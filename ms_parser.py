import threading
import time
import traceback

import requests
from bs4 import BeautifulSoup as bs4
from openpyxl import Workbook
from selenium import webdriver
from progress.bar import IncrementalBar

from exists import exists

unusual = []
urls = []
errors = []
output = []

errors_url = [
    'http://mirsud-chr.ru/',
    'http://issinsky.pnz.msudrf.ru',
    'http://sakha14.yak.msudrf.ru',
    'http://len8.tyum.msudrf.ru'
]


def format_tuple(tuple_):
    out = []
    for i in tuple_:
        out.append(i.replace('\n', '').replace(u'\xa0', u' '))
    return out


def parse_tatar(driver):
    soup = bs4(driver.page_source, 'html.parser')
    name = soup.find('span', class_='header').text
    fio = ''
    email = ''
    address = ''
    phone = ''

    results = soup.find('table', id='detail').find_all('td')
    for tag in results:
        if tag.text == 'ФИО Мирового судьи: ':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'E-mail: ':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Адрес: ':
            address = results[results.index(tag) + 1].text

        elif tag.text == 'Телефон судебного участка: ':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_mor(driver):
    soup = bs4(driver.page_source, 'html.parser')

    name = soup.find('a', class_='text-center text-md-left text-lg-left text-xl-left Montserrat-Medium menu').text
    address = soup.find('div', attrs={'data-bind': 'text: Address'}).text
    fio = ''
    email = ''
    phone = ''

    results = soup.find('div', attrs={'data-bind': 'foreach: SudArray'}).find_all()
    for tag in results:
        if tag.text == 'Мировой судья':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'Email: ':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Телефон: ':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_pskov(driver):
    soup = bs4(driver.page_source, 'html.parser')
    name = soup.find('div', class_='content_text').find('table').find('h1').text
    fio = ''
    email = ''
    address = ''
    phone = ''

    results = soup.find('div', class_='content_text').find('table').find_all('td')
    for tag in results:
        if 'Мировой судья:' in tag.text:
            fio = tag.text.replace('Мировой судья:', '')

        elif 'E-mail:' in tag.text:
            email = tag.text.replace('', '')

        elif 'Адрес:' in tag.text:
            address = tag.text.replace('', '')

        elif 'Телефон:' in tag.text:
            phone = tag.text.replace('', '')

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_sev(driver):
    soup = bs4(driver.page_source, 'html.parser')
    name = 'Севастополь ' + soup.find('span', class_='subheaderb').text
    fio = ''
    email = ''
    address = ''
    phone = ''

    results = soup.find('table', id='detail').find_all('td')
    for tag in results:
        if tag.text == 'ФИО Мирового судьи: ':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'E-mail: ':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Адрес: ':
            address = results[results.index(tag) + 1].text

        elif tag.text == 'Телефон для справок: ':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_crimea(driver):
    soup = bs4(driver.page_source, 'html.parser')
    print(soup)
    name = ''
    # name = 'Республика Крым ' + soup.find('span', class_='subheaderb').text
    fio = ''
    email = ''
    address = ''
    phone = ''

    results = soup.find('table', id='detail').find_all('td')
    for tag in results:
        if tag.text == 'ФИО Мирового судьи: ':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'E-mail: ':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Адрес: ':
            address = results[results.index(tag) + 1].text

        elif tag.text == 'Телефон для справок: ':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_hm(driver):
    soup = bs4(driver.page_source, 'html.parser')
    name = soup.find('div', class_='MM').find('h1').text
    fio = ''
    email = ''
    address = ''
    phone = ''

    results = soup.find('table', id='detail').find_all('td')
    for tag in results:
        # print(tag.text)
        if tag.text == 'Судья: ':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'E-mail: ':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Адрес судебного участка: ':
            address = results[results.index(tag) + 1].text

        elif tag.text == 'Телефон: ':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_24(driver):
    driver.get(driver.current_url + 'o-sude/index.php')
    soup = bs4(driver.page_source, 'html.parser')
    name = soup.find('div', style='position: absolute; margin-left: 85px;margin-top:-40px; font-size: 16px; line-height: 1.2; font-weight: 900;').text
    fio = ''
    email = ''
    address = ''
    phone = ''
    try:
        address = soup.find('div', class_="col col-mb-12 col-6 col-dt-3 mt10 col-margin-bottom").text.replace('Адрес судебного участка', '') + 'Красноярский край'
    except:
        address = ''

    results = soup.find('div', class_='white-box padding-box').find_all('td')
    for tag in results:
        # print(tag.text)
        if 'Телефон канцелярии:' in tag.text:
            phone = results[results.index(tag) + 1].text.replace('\t', '')

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_spb(driver):
    soup = bs4(driver.page_source, 'html.parser')
    name = 'Санкт-Петербург ' + soup.find('h1', class_='title').text
    address = soup.find('div', class_='adress-fact').find('p').text
    phone = soup.find('div', class_='telfax').find('p').text
    email = soup.find('a', class_='link__mail').text
    fio = ''

    results = soup.find('article', class_='about-sector').find('div', class_='col-lg-6').find_all()
    for tag in results:
        if tag.text == 'Судья':
            fio = results[results.index(tag) + 1].text
            break

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_orenburg(driver):
    soup = bs4(driver.page_source, 'html.parser')
    # print(soup)
    name = soup.find('div', class_='text-logo').text
    results = soup.find_all('div', style='margin-bottom: 1rem;')
    email = ''
    try:
        address = soup.find('div', class_="footer-contacts").find('div').text
    except:
        address = ''

    phone = ''
    for tag in results:
        if tag.find_all('div')[0].text == 'Секретарь суда':
            for row in tag.find_all('div'):
                text = row.text
                if 'Телефон: ' in text:
                    phone = text.replace('Телефон: ', '').replace('/n', '')
                elif 'email: ' in text:
                    email = text.replace('Электронная почта: ', '').replace('/n', '')
    if phone == '':
        try:
            divs = soup.find('div', class_='card-body').find_all('div')
            for div in divs:
                text = div.text
                if 'Телефон: ' in text:
                    phone = text.replace('Телефон: ', '').replace('/n', '')
        except:
            pass

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def parse_mos(driver):
    soup = bs4(driver.page_source, 'html.parser')
    results = soup.find_all('td')
    fio = ''
    email = ''
    address = ''
    phone = ''
    name = 'Москва ' + soup.find('section', class_='middle_bar inner_nosider').find('h1').text
    for tag in results:
        if tag.text == 'ФИО Мирового судьи':
            fio = results[results.index(tag) + 1].text

        elif tag.text == 'E-mail':
            email = results[results.index(tag) + 1].text

        elif tag.text == 'Адрес':
            address = 'Москва ' + results[results.index(tag) + 1].text

        elif tag.text == 'Телефон судебного участка':
            phone = results[results.index(tag) + 1].text

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def check_unusual(url, check_unknown=False):
    if 'mos-sud.ru' in url:
        return True
    elif 'kodms.ru' in url:
        return True
    elif 'mirsud.spb.ru' in url:
        return True
    elif 'mirsud86.ru' in url:
        return True
    elif 'mirsud82.rk.gov.ru' in url:
        return True
    elif 'mirsud.sev.gov.ru' in url:
        return True
    elif 'mirsud.pskov.ru' in url:
        return True
    elif 'mirsud.e-mordovia.ru' in url:
        return True
    elif 'mirsud.tatar.ru' in url:
        return True
    else:
        if check_unknown:
            if 'msudrf.ru' in url:
                return True
            else:
                return False
        return False


def parse_unusual(driver, url):
    if 'mos-sud.ru' in url:
        parse_mos(driver)
    elif 'kodms.ru' in url:
        try:
            driver.find_element_by_class_name('no_more').click()
        except:
            print('no_btn')
            pass
        # input()
        your_element = driver.find_element_by_tag_name('html').get_attribute("outerHTML")
        parse_orenburg(driver)
    elif 'mirsud.spb.ru' in url:
        parse_spb(driver)
    elif 'mirsud24.ru' in url:
        parse_24(driver)
    elif 'mirsud86.ru' in url:
        time.sleep(0.2)
        parse_hm(driver)
    elif 'mirsud82.rk.gov.ru' in url:
        # parse_crimea(driver)
        pass
    elif 'mirsud.sev.gov.ru' in url:
        time.sleep(0.2)
        parse_sev(driver)
    elif 'mirsud.pskov.ru' in url:
        time.sleep(0.2)
        parse_pskov(driver)
    elif 'mirsud.e-mordovia.ru' in url:
        time.sleep(0.3)
        parse_mor(driver)
    elif 'mirsud.tatar.ru' in url:
        time.sleep(0.2)
        parse_tatar(driver)
    else:
        pass


def parse(driver):
    email = ''
    soup = bs4(driver.page_source, 'html.parser')
    name = soup.find('span', id='court_name').text
    try:
        address = soup.find('p', id='court_address').text
    except:
        address = ''
    try:
        email = soup.find('p', id='court_email').text
    except:
        block = soup.find_all('div', class_='info-block')[1].find_all()
        for i in block:
            if i.text == 'E-mail':
                email = block[block.index(i) + 1].text

    phone = None
    fio = None

    block = soup.find('div', class_='info-block')
    contacts = block.find_all()
    for tag in contacts:
        text = tag.text.lower().replace(' ', '')
        if text == 'мировойсудья':
            fio = contacts[contacts.index(tag) + 1].text
            if phone is None:
                try:
                    phone = contacts[contacts.index(tag) + 3].find('span', class_='right').text
                except:
                    pass
            continue
        elif text == 'секретарьсудебногоучастка':
            try:
                phone = contacts[contacts.index(tag) + 3].find('span', class_='right').text
            except:
                pass

        elif text == 'секретарьсудебногозаседания':
            if phone is None:
                try:
                    phone = contacts[contacts.index(tag) + 3].find('span', class_='right').text
                except:
                    pass

    if not phone:
        try:
            phone = block.find('p', class_='person-phone').find('span', class_='right').text
        except:
            phone = ''

    if not fio:
        for tag in contacts:
            text = tag.text.lower().replace(' ', '')
            if text == 'и.о.мировогосудьи':
                fio = contacts[contacts.index(tag) + 1].text
                break
            elif text == 'судья':
                fio = contacts[contacts.index(tag) + 1].text
                break
    if not fio:
        fio = ''

    out = format_tuple((name, address, email, phone, driver.current_url))
    print(out)
    output.append(out)


def driver_thread(urls_local, unusual_only=False):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    for url in urls_local:
        try:
            # url = html.find('a', target='_blank')['href']
            if url in errors:
                urls.remove(url)
                continue
            if unusual_only:
                if not check_unusual(url):
                    urls.remove(url)
                    continue
            print(url, flush=True)
            driver.get(url)
            if not unusual_only:
                resp = driver.page_source
                soup = bs4(resp, 'html.parser')
                address = soup.find('div', class_='address-block')
                if not address:
                    parse_unusual(driver, url)
                else:
                    if address.find('h2').text != 'Адрес':
                        parse_unusual(driver, url)
                    else:
                        parse(driver)
            else:
                parse_unusual(driver, url)

            urls.remove(url)
        except Exception as e:
            # url = html.find('a', target='_blank')['href']
            print(traceback.format_exc(), flush=True)
            print('err ', url, flush=True)
            errors.append(url)
    return


def main_thread(unusual_only=False):
    threads = []
    length = len(urls)
    step = length // 7
    for i in range(6):
        threads.append(threading.Thread(target=driver_thread, args=(urls[i * step:(i + 1) * step], unusual_only)))
    threads.append(threading.Thread(target=driver_thread, args=(urls[length-step:], unusual_only)))
    for thread in threads:
        thread.start()

    while True:
        alive = False
        print(len(urls), flush=True)
        for thread in threads:
            if thread.is_alive():
                time.sleep(2)
                alive = True
                break
        if alive:
            continue
        return


def main(unusual_only=False):
    global urls
    url = 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj=0'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    resp = driver.page_source
    soup = bs4(resp, 'html.parser')
    urls = soup.find('table', class_='msSearchResultTbl').find_all('tr')
    print(len(urls))

    urls_2 = []

    for html in urls:
        url = html.find('a', target='_blank')['href']
        urls_2.append(url)

    urls = urls_2

    urls_3 = []
    for url in urls:
        if 'mirsud24.ru' in url:
            urls_3.append(url)
                # print(url)
    #
    # return

    urls = urls_3

    # return
    main_thread(unusual_only)

    name = 'task2_new.xlsx'
    wb = Workbook()
    wb.create_sheet('sheet1')
    ws = wb['sheet1']

    for row in output:
        ws.append(row)

    wb.save(name)

    print('--------------unusual-------------------')
    for url in unusual:
        print(url)

    print('---------------errors-------------------')
    for url in errors:
        print(url)


if __name__ == '__main__':
    main()
