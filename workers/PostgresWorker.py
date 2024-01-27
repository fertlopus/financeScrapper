import os
import queue
import threading
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        if 'output_queue' in kwargs:
            kwargs.pop('output_queue', None)
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            try:
                value = self._input_queue.get(timeout = 10)
            except queue.Empty:
                print('Queue is empty. Timeout reached.')
                break
            if value is 'DONE':
                break
            ticker, price, extracted_time = value
            postgres_worker = PostgresWorker(ticker, price, extracted_time)
            postgres_worker.put_to_database()


class PostgresWorker:
    def __init__(self, ticker, price, extracted_time):
        self._ticker = ticker
        self._price = price
        self._extracted_time = extracted_time

        self._PG_USER = os.environ.get('PG_USER') or 'postgres'
        self._PG_PW = os.environ.get('PG_PW') or ''
        self._PG_HOST = os.environ.get('PG_HOST') or 'localhost'
        self._PG_DB = os.environ.get('PG_DB') or 'postgres'

        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}')

    @staticmethod
    def _create_input_query():
        query = """INSERT INTO prices (symbol, price, extracted_time) 
        VALUES (:ticker, :price, :extracted_time)"""
        return query

    def put_to_database(self):
        insert_query = self._create_input_query()
        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {'ticker': self._ticker,
                                              'price': self,
                                              'extracted_time': str(self._extracted_time)})
