from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
print("=" * 50, f'START {datetime.now().strftime("%dd %mm %Yy %H:%M:%S")} (GMT+03:00)', "=" * 50)
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
service = Service('/usr/local/bin/geckodriver')
options.binary = FirefoxBinary('/opt/firefox/firefox')
driver = webdriver.Firefox(options=options, service=service)

print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: The driver started successfully')
driver.get("https://mxtoolbox.com/")
print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Opening a page')
with open('domain.conf', 'r') as f:
    domain_list = [line.strip() for line in f.readlines()]

new_dict = {}

for domain in domain_list:
    new_dict[domain] = {}
    ip_list = []
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input').clear()
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input').send_keys(domain)
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/input').click()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Search {domain} domain')
    time.sleep(10)
    page_source = driver.page_source  
    soup = BeautifulSoup(page_source, "lxml")
    table = soup.find('div', 'tool-result-body')
    ip_addresses = table.find_all(class_='table-column-IP_Address')

    for ip_address in ip_addresses:
        ip_list.append(ip_address.get_text(strip=True).split()[0][:-7])
    
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/input').clear()
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/button').click()
    driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/ul/div/li[2]').click()

    for ip in ip_list:
        print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Searching {ip} ip')

        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/input').send_keys(ip)
        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/a').click()
        time.sleep(8)
        page = driver.page_source
        soup = BeautifulSoup(page, "lxml")
        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/input').clear()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        table = soup.find('table', 'table table-striped table-bordered table-condensed tool-result-table')
        tables = table.find('tbody')
        row_list = tables.find_all('tr')
        names = []

        for row in row_list:
            img_tag = row.find('img')
            name = row.find('td', class_='table-column-Name').text
            if img_tag and img_tag['alt'] == 'Status Problem':
                names.append(name)
        new_dict[domain][ip] = names if names else 'Clear'
    driver.back()
driver.quit()
with open('/opt/data_files/mail_ban.json', 'w') as f:
    json.dump(new_dict, f, indent=5)

print("=" * 50, f'PARSE {datetime.now().strftime("%dd %mm %Yy %H:%M:%S")} (GMT+03:00)', "=" * 50)
