import hashlib
import json
import requests
import os

from typing import Optional, Callable, Union
from datetime import datetime
from estela_queue_adapter import get_producer_interface
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests_wrapper.http import EstelaResponse, EstelaRequest
from estela_requests_wrapper.exceptions import UnexpectedResponseType
from requests import Response

default_requests = requests


def parse_time(date: datetime = None) -> str:
    if date is None:
        date = datetime.now()
    parsed_time = date.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    return parsed_time


def decode_job():
    job_data = os.getenv("JOB_INFO", "")
    if job_data.startswith("{"):
        return json.loads(job_data)

def get_producer(producer: Optional[ProducerInterface]) -> ProducerInterface:
    return producer or get_producer_interface()

def get_requests(_requests: Optional[Callable]) -> Callable:
    return _requests or default_requests

def get_estela_response(response: Union[Response, any]) -> EstelaResponse:
    if isinstance(response, Response):
        return EstelaResponse(
            response.url,
            response.content,
            response.text,
            response.status_code,
            EstelaRequest(response.request),
            len(response.text),
            hashlib.sha1(response.text.encode("UTF-8")).hexdigest(),
            response.elapsed,
        )
    raise UnexpectedResponseType("The response type is not supported")
