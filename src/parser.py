# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def parse(host):
    all_data = []
    url = 'https://a.pr-cy.ru/' + host + '/'
    # Html Code Parsing
    try:
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.text
    except:
        return 'Wrong Host!'
    # Html Processig
    soup = BeautifulSoup(html, 'lxml')
    try:
        line = soup.find(
            'table', class_='table-clear table-content-test').find('tbody').find_all('tr')
    except:
        return 'Wrong Host!'    
    # Views Parse
    td = line[0].find_all('td')
    day1 = td[1].text.replace('\xa0', ' ')
    week1 = td[2].text.replace('\xa0', ' ')
    month1 = td[3].text.replace('\xa0', ' ')
    views = [day1, week1, month1]
    all_data.append(views)
    # Visits Parse
    td = line[1].find_all('td')
    day2 = td[1].text.replace('\xa0', ' ')
    week2 = td[2].text.replace('\xa0', ' ')
    month2 = td[3].text.replace('\xa0', ' ')
    visits = [day2, week2, month2]
    all_data.append(visits)
    # Countries Parse
    line = soup.find_all('div', class_="analysis-test__content")
    for t in line:
        e = t.find('p')
        try:
            if e.text == 'Примерная география посетителей сайта за последние 30 дней.':
                global line2
                line2 = t
                break
        except:
            continue
    line2 = line2.find('table', class_='table-clear').find('tbody').find_all('tr')
    countries = []
    for tr in line2:
        td = tr.find_all('td')
        countries.append(td[0].text)
    all_data.append(countries)
    # Sites Parse
    sites = []
    try:
        line = soup.find('table', class_='table-clear', style='margin-top:0').find('tbody').find_all('tr')
        for tr in line:
            td = tr.find('td')
            sites.append(td.text)
    except:
        pass
    if len(sites) == 0:
        sites.append('Похожие сайты не найдены!')
    all_data.append(sites)
    # Ip History Parse
    ip_history = []
    line = soup.find('div', id='sameIps').find('div', class_='table-responsive').find('tbody').find_all('tr')
    #print(line)
    for tr in line:
        ip_history.append(tr.find('td').text.strip())
    all_data.append(ip_history)
    # Return All_data
    return all_data

