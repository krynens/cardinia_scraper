import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import scraperwiki

today = datetime.today()

url = 'https://www.cardinia.vic.gov.au/advertisedplanningapplications'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('tbody')
rows = table.find_all('tr')

for row in rows:
    record = {}
    record['address'] = row.find_all('td')[2].text
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find_all('td')[1].text
    record['council_reference'] = row.find_all('td')[0].text
    record['info_url'] = str(row.find_all('td')[0]).split('"')[1]
    on_notice_to_raw = row.find_all('td')[3].text
    record['on_notice_to'] = datetime.strptime(on_notice_to_raw, "%d %B %Y").strftime("%Y-%m-%d")

    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
