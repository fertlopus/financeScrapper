import threading
import requests
from bs4 import BeautifulSoup


class WikiWorkerMasterScheduler(threading.Thread):
    def __init__(self, output_queue, **kwargs):
        if 'input_queue' in kwargs:
            kwargs.pop('input_queue')
        self._input_values = kwargs.pop('entries')
        temp_queue = output_queue
        if not isinstance(temp_queue, list):
            temp_queue = [temp_queue]
        self._output_queue = temp_queue
        super(WikiWorkerMasterScheduler, self).__init__(**kwargs)
        self.start()

    def run(self):
        for entry in self._input_values:
            wikiWorker = WikiWorker(entry)
            ticker_counter = 0
            for ticker in wikiWorker.get_sp500_companies():
                for output_queue in self._output_queue:
                    output_queue.put(ticker)
                ticker_counter += 1


class WikiWorker(object):
    def __init__(self, url):
        # URL to the Wikipedia page with S&P500 companies list (FYI: link can be changed)
        self._url = url

    @staticmethod
    def _get_companies_symbols(html_page):
        soup = BeautifulSoup(html_page, 'lxml')
        # FYI: if table id changes you can inspect the html table id and paste new name here
        contents = soup.find(id = 'constituents')
        table_rows = contents.find_all('tr')
        for table_row in table_rows[1:]:
            ticker = table_row.find('td').text.strip('\n')
            yield ticker

    def get_sp500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Response Code: ", response.status_code)
            return []
        yield from self._get_companies_symbols(html_page = response.text)
