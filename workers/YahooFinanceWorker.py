import queue
import threading
import requests
from lxml import html
import datetime
import time
import random


class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(YahooFinanceScheduler, self).__init__(**kwargs)
        # take the input thread and start the execution
        self._in_queue = input_queue
        temp_queue = output_queue
        if not isinstance(temp_queue, list):
            temp_queue = [temp_queue]
        self._output_queue = temp_queue
        self.start()

    def run(self):
        while True:
            # Blocking operation until value is returned
            try:
                value = self._in_queue.get(timeout = 10)
            except queue.Empty:
                print("Yahoo Scheduler has exited due to queue empty")
                break
            if value == 'DONE':
                for output_queue in self._output_queue:
                    output_queue.put('DONE')
                break

            yahoo_finance_worker = YahooFinanceWorker(ticker = value)
            price = yahoo_finance_worker.get_ticker_price()
            for output_queue in self._output_queue:
                output_values = (value, price, datetime.datetime.utcnow())
                output_queue.put(output_values)
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
