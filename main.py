from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorker import YahooFinanceScheduler
from multiprocessing import Queue
from workers.PostgresWorker import PostgresMasterScheduler
from yaml_run import YamlPipelineExecutor
import time
import os


def main():
    pipeline_location = os.environ.get('PIPELINE_LOCATION')
    if pipeline_location is None:
        print('Pipeline location not defined')
        exit(1)
    scraper_start_time = time.time()
    yamlPipelineExecutor = YamlPipelineExecutor(pipeline_location = pipeline_location)
    yamlPipelineExecutor.start()
    yamlPipelineExecutor.join()
    print('Extracting time took:', round(time.time() - scraper_start_time, 1))


if __name__ == '__main__':
    main()
