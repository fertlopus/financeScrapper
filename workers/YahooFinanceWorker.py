import threading
import requests
from lxml import html
import time
import random


class YahooFinanceWorker(threading.Thread):
    def __init__(self, ticker, **kwargs):
        super(YahooFinanceWorker, self).__init__(**kwargs)
        self._ticker = ticker
        self._base_url = "https://finance.yahoo.com/quote/"
        self._get_url = f"{self._base_url}{self._ticker}"
        self.start()

    def run(self):
        time.sleep(3 * random.random())
        response = requests.get(self._get_url)
        if response.status_code == 200:
            html_content = html.fromstring(response.text)
            price = html_content.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]')[0].text
            price = float(price.replace(',', ''))
            print(price)
            return price
        else:
            pass
