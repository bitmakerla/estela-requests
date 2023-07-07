# Estela Requests

## Introduction

Estela Requests is a Python library that provides enhanced functionality for making HTTP requests and seamlessly integrates with [estela](https://github.com/bitmakerla/estela), an open-source project that implements a platform for running spiders in-house or in the cloud, you can learn more about it [here](https://estela.bitmaker.la/docs/). This documentation provides a comprehensive overview of the Estela Requests library, installation instructions, and useful usage examples.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic usage](#basic-usage)
  - [Extend Estela Requests](#extend-estela-requests-beta)
- [More](#more)

## Installation

To install Estela Requests, you can use pip, the Python package manager. Open your terminal or command prompt and run the following command:

```shell
pip install estela-requests@git+https://github.com/bitmakerla/estela-requests.git
```

Also, you can clone the repository and install from there, running the following command:

```shell
git clone git@github.com:bitmakerla/estela-requests.git
cd estela-requests
pip install -e .
```

## Usage

### Basic Usage

Here's an example of how to use Estela Requests to scrape the site http://quotes.toscrape.com and send items to Estela:

```python
from bs4 import BeautifulSoup

from estela_requests import EstelaRequests
from estela_requests.estela_hub import EstelaHub
from urllib.parse import urljoin

with EstelaRequests.from_estela_hub(EstelaHub.create_from_settings()) as requests:
    spider_name = "quotes_toscrape"
    # Send a GET request to the website
    def parse_quotes(url):
        response = requests.get(url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the desired information from the parsed HTML
        quotes = []
        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            quotes.append({"text": text, "author": author, "tags": tags})

        # Print the extracted information
        for quote in quotes:
            item = {
                "quote": quote["text"],
                "author": quote["author"],
                "tags": ','.join(quote["tags"]),
            }
            requests.send_item(item)
        try:
            next = soup.find("li", class_="next").find("a").get("href")
        except AttributeError:
            next = None
        if next:
            parse_quotes(urljoin(url, next))
    
    if __name__ == "__main__":
        parse_quotes("http://quotes.toscrape.com/")
```

First we need to import the `EstelaRequests` and `EstelaHub` classes:

```python
from estela_requests import EstelaRequests
from estela_requests.estela_hub import EstelaHub
```

Once imported, you can create a `EstelaRequests` context manager:

```python
with EstelaRequests.from_estela_hub(EstelaHub.create_from_settings()) as requests:
```

To assign a name for the spider in estela you should declare the `spider_name` with the desired name, e.g.

```python
spider_name = "quotes_toscrape"
```

Finally if you want to yield items you should use `send_item` method:

```python
requests.send_item(item)
```

### Extend Estela Requests (BETA)

Estela Requests can be easily customized by creating a settings.py file in the directory where you run your code:
```python
import logging

from estela_requests.request_interfaces import RequestsInterface
from estela_queue_adapter.get_interface import get_producer_interface
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.log_helpers.handlers import KafkaLogHandler
from estela_requests.item_pipeline.exporter import KafkaItemExporter, StdoutItemExporter

ESTELA_PRODUCER = get_producer_interface()  # ESTELA_PRODUCER is a queue producer(e.g. kafka producer) that will be used to communicate estela-requests 
ESTELA_PRODUCER.get_connection()            # with estela
HTTP_CLIENT = RequestsInterface()           # HTTP Requests interface that will be used, at the moment we just have RequestsInterface(requests library)
ESTELA_API_HOST = ""                        # This code will be set by estela, you shouldn't move it at least you want to test things
ESTELA_SPIDER_JOB = ""                      # Same as above
ESTELA_SPIDER_ARGS = ""                     # Same as above, at the moment estela-requests doesn't support arguments.
ESTELA_ITEM_PIPELINES = []                  # Item Pipelines to use, i.e. a DateItemPipeline that will add the timestamp to the item.
                                            # Check ItemPipelineInterface to create a new item pipeline.
ESTELA_ITEM_EXPORTERS = [KafkaItemExporter] # Item Exporter to use. Where to export, send the data. Check ItemExporterInterface to create a new                                                     # exporter.
ESTELA_LOG_LEVEL = logging.DEBUG            # Logging Level
ESTELA_LOG_FLAG = 'kafka'                   # This will be removed in future releases.
ESTELA_NOISY_LIBRARIES = []                 # A list of noisy library that you want to turn off.
ESTELA_MIDDLEWARES = [RequestsHistoryMiddleware, StatsMiddleware, SpiderStatusMiddleware]   # Middlewares to use, check MiddlewareInterface to create a new one. 
JOB_STATS_TOPIC = "job_stats"               # Topic name for job stats. 
JOB_ITEMS_TOPIC = "job_items"               # Topic name for job items.
JOB_REQUESTS_TOPIC = "job_requests"         # Topic name for job requests.
JOB_LOGS_TOPIC = "job_logs"                 # Topic name for job logs
```
## More

For more details and information about the Estela project, please refer to the [Estela documentation](https://estela.bitmaker.la/docs/). The documentation provides comprehensive information about the project and its functionalities.
