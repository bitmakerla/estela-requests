import hashlib
import json
import requests
import os

from typing import Optional, Callable, Union
from datetime import datetime
from estela_queue_adapter import get_producer_interface
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests_wrapper.http import EstelaResponse, EstelaRequest
from estela_requests_wrapper.request_interfaces import HttpRequestInterface, RequestsInterface
from estela_requests_wrapper.exceptions import UnexpectedResponseType
from requests import Response

default_requests = requests


def parse_time(date: datetime = None) -> str:
    """Parse the time to the format used in the Estela platform."""
    if date is None:
        date = datetime.now()
    parsed_time = date.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    return parsed_time


def decode_job():
    """Decode the job data from the environment variable."""
    job_data = os.getenv("JOB_INFO", "")
    if job_data.startswith("{"):
        return json.loads(job_data)
    
def get_metadata(metadata: Optional[dict] = None) -> dict:
    """Get the metadata from the environment variables if metadata does not exist.
    
    args:
        metadata (Optional[dict]): The metadata.
    """
    return metadata or decode_job()["key"]


def get_producer(producer: Optional[ProducerInterface]) -> ProducerInterface:
    """Get the producer interface.
    
    If the producer is not passed as an argument, it will try to get it from the environment variables.

    Args:
        producer (Optional[ProducerInterface]): The producer interface.
    """
    return producer or get_producer_interface()

def get_http_client(http_client: Optional[HttpRequestInterface]) -> Callable:
    """Get the http client."""
    return http_client or RequestsInterface()

def get_requests(_requests: Optional[Callable]) -> Callable:
    """Get the requests library."""
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

