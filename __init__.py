from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import csv


if __name__ == '__main__':
    url = '<URL to website to scrape>'
    # driver = webdriver.PhantomJS('<Path to PhantomJS>')
    # driver.set_window_size(1124, 850)
    driver = webdriver.Firefox()
    driver.get(url)

    # Force page to scroll to bottom
    i = 0
    while i < 22:
        rand = random.uniform(0.5, 2)
        time.sleep(rand)
        bg = driver.find_element_by_css_selector('body')
        bg.send_keys(Keys.PAGE_DOWN)
        bg.send_keys(Keys.PAGE_DOWN)
        bg.send_keys(Keys.PAGE_DOWN)
        time.sleep(10)
        i += 1

    # Get page source and parse ul for company-list
    html = driver.page_source
    soup = BeautifulSoup(html)
    companyList = soup.find('ul', {'class', 'company-list'})
    lis = companyList.find_all('li')

    # Open CSV File
    plopper = csv.writer(open('f500.csv', 'w'))
    plopper.writerow(['rank', 'CompanyName', 'revenueInMillions', 'city', 'state'])

    for li in lis:
        companyURL = ''
        companyURL = urljoin(url, li.find('a')['href'])
        spans = li.find_all('span')
        rank = spans[0].get_text()
        companyName = spans[1].get_text()
        revenueInMillions = spans[2].get_text()

        # Get Company Page
        if companyURL != '' # and int(rank) >= 902:
            driver.get(companyURL)
            companyRand = random.uniform(5, 20)
            time.sleep(companyRand)
            companyHTML = driver.page_source
            companySoup = BeautifulSoup(companyHTML)
            card = companySoup.find('div', {'class', 'row company-info-card-table'})
            companyHQLoc = card.find_all('div')[7].find_all('p')[1].get_text()
            city, state = companyHQLoc.split(',')
            print(rank, companyName, revenueInMillions, city, state)

            # Write row to CSV
            plopper.writerow([rank, companyName, revenueInMillions, city, state])



