"""Wrapper that allows to send requests in Estela platform and log them in the queue platform."""
import logging
import os

from typing import Any, Optional, Union, Callable, Dict, List
from requests import Response, Session, Request
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_queue_adapter import get_producer_interface
from estela_requests_wrapper.utils import get_producer, get_requests, get_estela_response
from estela_requests_wrapper.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests_wrapper.middlewares.stats import StatsMiddleware
from estela_requests_wrapper.http import EstelaResponse
from estela_requests_wrapper.request_interfaces import HttpRequestInterface


def apply_request_middlewares(func: Callable):
    def wrapper(wrapper_obj, *args, **kwargs) -> EstelaResponse:
        for mw in wrapper_obj.middlewares:
            mw.before_request(*args, **kwargs)

        response = func(wrapper_obj, *args, **kwargs)
        estela_response = get_estela_response(response)

        for mw in wrapper_obj.middlewares:
            mw.after_request(estela_response)

        return response

    return wrapper

class EstelaWrapper:

    http_client: HttpRequestInterface

    def __init__(self,
                 producer: Optional[ProducerInterface] = None,
                 metadata: Optional[Dict] = {},
                 http_client: Optional[HttpRequestInterface] = None) -> None:
        self.producer = get_producer(producer)
        self.metadata = metadata
        self.http_client = http_client
        if self.producer.get_connection():
            print("Successful connection to the queue platform")
        else:
            raise Exception("Could not connect to the queue platform") 
        self.middlewares = [
            RequestsHistoryMiddleware(self.producer, "job_requests", self.metadata),
            StatsMiddleware(self.producer, "job_stats", self.metadata),
        ]

    def _get_http_client(self):
        return self.http_client
    
    @apply_request_middlewares
    def get(self, *args, **kwargs):
        return self.http_client.get(*args, **kwargs)
    
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
    
    def call_middlewares(self):
        for mw in self.middlewares:
            mw.after_session()

    def __del__(self):
        self.producer.flush()
        self.producer.close()


# class EstelaRequestsWrapper:
#     producer = get_producer_interface()
#     #TODO anadir un handler que tenga soft y hard aviso cuando no esten
#     # los parametros necesarios para subir el proyecto a estela.
#     # project_id = 68b589b3-6b2c-4b39-beb8-1d45a496f6ef
#     def __init__(self, spider_name: str) -> None:
#         if self.producer.get_connection():
#             print("Successful connection to the queue platform.")
#         else:
#             raise Exception("Could not connect to the queue platform.")
#         self.spider_name = spider_name
#         # Sacar el SID, JID y PID de las varibles y entorno.
#         self.jid = "3.155.99b2627d-104f-425d-9158-d12fe8d1a245"
#         super().__init__()
   
#     # It could be seen as middleware
#     # esto debe ser llamado desde el principio probablemente.
#     # 
#     def url_logger(self, func):
#         def wrapper(*args, **kwargs):
#             print(f"Realizando solicitud a: {args[2]}")
#             response = func(*args, **kwargs)
#             data = {
#                 "jid": self.jid,
#                 "payload": {
#                     "url": response.url,
#                     "status": int(response.status_code),
#                     "method": response.request.method,
#                     "duration": int(10),
#                     "time": "time",
#                     "response_size": len(response.content),
#                     "fingerprint": "adsa",
#                 },
#             }
#             self.producer.send("job_requests", data)
#             return response
#         return wrapper
    
#     def __del__(self):
#         self.producer.flush()
#         self.producer.close()


# wrapper = EstelaRequestsWrapper("default")

# class RequestsWrapperSession(Session):
#     @wrapper.url_logger
#     def request(self, method: str | bytes, url: str, *args, **kwargs) -> Response:
#         return super().request(method, url, *args, **kwargs)
    
#     def send_item(self, item):
#         wrapper.producer.send("job_items", item)
#         return item
