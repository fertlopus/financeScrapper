import requests
from bs4 import BeautifulSoup


class WikiWorker(object):
    def __init__(self):
        # URL to the Wikipedia page with S&P500 companies list (FYI: link can be changed)
        self._url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

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
