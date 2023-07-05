import hashlib
import json
import requests
import os

from datetime import datetime
from estela_requests.estela_http import EstelaResponse, EstelaHttpRequest
from requests import Response

default_requests = requests


def elapsed_seconds_time(end_time, start_time):
    elapsed = datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S.%f") - datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S.%f")
    return float(f"{elapsed.seconds}.{elapsed.microseconds}")

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

def get_estela_response(response: Response) -> EstelaResponse:
    # It should be extended to support another resposne types
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
