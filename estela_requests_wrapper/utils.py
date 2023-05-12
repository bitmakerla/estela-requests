import os 
import json
import requests

from typing import Optional, Callable
from datetime import datetime
from estela_queue_adapter import get_producer_interface
from estela_queue_adapter.abc_producer import ProducerInterface

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
