import hashlib
import json
import requests
import os

from typing import Optional, Callable, Union
from datetime import datetime
from estela_queue_adapter import get_producer_interface
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests.estela_http import EstelaResponse, EstelaHttpRequest
from estela_requests.request_interfaces import HttpRequestInterface, RequestsInterface
from estela_requests.exceptions import UnexpectedResponseType
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

def get_api_host(api_host: Optional[str] = None) -> str:
    """Get the API host from the environment variable."""
    return api_host or os.getenv("ESTELA_SPIDER_HOST")

def get_job(job: Optional[str] = None) -> str:
    return job or os.getenv("ESTELA_SPIDER_JOB")

def get_auth_token(auth_token: Optional[str] = None) -> str:
    return auth_token or os.getenv("ESTELA_AUTH_TOKEN")

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
            EstelaHttpRequest(response.request),
            len(response.text),
            hashlib.sha1(response.text.encode("UTF-8")).hexdigest(),
            response.elapsed,
        )
    raise UnexpectedResponseType("The response type is not supported")
