"""Wrapper that allows to send requests in Estela platform and log them in the queue platform."""
import logging
import os

from typing import Any, Optional, Union, Callable, Dict, List
from requests import Response, Session, Request
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_queue_adapter import get_producer_interface
from estela_requests.utils import get_producer, get_estela_response, get_metadata, get_http_client
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.http import EstelaResponse
from estela_requests.request_interfaces import HttpRequestInterface


def apply_request_middlewares(func: Callable):
    def wrapper(wrapper_obj, *args, **kwargs) -> EstelaResponse:
        for mw in wrapper_obj.middlewares:
            mw.before_request(*args, **kwargs)

        response = func(wrapper_obj, *args, **kwargs)
        estela_response = get_estela_response(response)

        for mw in wrapper_obj.middlewares:
            mw.after_request(estela_response, *args, **kwargs)

        return response

    return wrapper

class EstelaWrapper:

    http_client: HttpRequestInterface

    def __init__(self,
                 producer: Optional[ProducerInterface] = None,
                 metadata: Optional[Dict] = {},
                 http_client: Optional[HttpRequestInterface] = None) -> None:
        self.producer = get_producer(producer)
        self.metadata = get_metadata(metadata)
        self.http_client = get_http_client(http_client)
        if self.producer.get_connection():
            print("Successful connection to the queue platform")
        else:
            raise Exception("Could not connect to the qbueue platform") 
        self.middlewares = [
            RequestsHistoryMiddleware(self.producer, "job_requests", self.metadata),
            StatsMiddleware(self.producer, "job_stats", self.metadata),
        ]

    def _get_http_client(self):
        return self.http_client
    
    #@apply_request_middlewares
    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)
    
    @apply_request_middlewares
    def request(self, *args, **kwargs):
        return self.http_client.request(*args, **kwargs)
    
    def send_item(self, item: Dict, *args, **kwargs):
        estela_item = {
            **self.metadata,
            "payload": item,
            "unique": True,
        }
        self.producer.send("job_items", estela_item)
        return item
 
    def call_before_session_middlewares(self):
        for mw in self.middlewares:
            mw.before_session()

    def call_after_session_middlewares(self):
        for mw in self.middlewares:
            mw.after_session()

    def __del__(self):
        self.producer.flush()
        self.producer.close()
