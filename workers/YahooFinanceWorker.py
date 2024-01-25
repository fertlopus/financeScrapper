import threading
import requests
from lxml import html
import time
import random


class YahooFinanceScheduler(threading.Thread):
    def __init__(self, in_queue, **kwargs):
        super(YahooFinanceScheduler, self).__init__(**kwargs)
        # take the input thread and start the execution
        self._in_queue = in_queue
        self.start()

    def run(self):
        while True:
            # Blocking operation until value is returned
            value = self._in_queue.get()
            if value == 'DONE':
                break

            yahoo_finance_worker = YahooFinanceWorker(ticker = value)
            price = yahoo_finance_worker.get_ticker_price()
            time.sleep(random.random())


class YahooFinanceWorker:
    def __init__(self, ticker, **kwargs):
        self._ticker = ticker
        self._base_url = "https://finance.yahoo.com/quote/"
        self._get_url = f"{self._base_url}{self._ticker}"

    def get_ticker_price(self):
        response = requests.get(self._get_url)
        if response.status_code == 200:
            html_content = html.fromstring(response.text)
            price = html_content.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]')[0].text
            price = float(price.replace(',', ''))
            return price
        else:
            pass
