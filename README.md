# The WikiPedia and YahooFinance Scrapper for Time Series Data

---

Concurrency experiment on parsing the stock price data from the yahoo finance web service. Using multithreading approach the app gets the data from s&p 500 companies list. Not a production ready application, just recap of multithreading approaches to data scrapping.

![img](/src/imgs/logo.png)

---

### Requirements:

---

* Python >= 3.7
* Install dependencies using `pipenv` or vanilla `pip` package managers (reuirements.txt and Pipfile files are provided)

---

### Database settings for saving tickers data:

---
_Requirements: postgres x.x_

_host: localhost_

Create db and table for saving the data:

```postgresql
CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY NOT NULL,
    ticker TEXT,
    price FLOAT,
    insert_date TIMESTAMP
);
```

Edit the file env.cfg (add your db settings and credentials).

---
