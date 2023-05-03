import requests
import logging
from sys import argv
# Habilitar el registro de errores de Requests

requests_log = logging.getLogger('requests')
requests_log.setLevel(logging.DEBUG)

response = requests.get(argv[1], timeout=10)
response.raise_for_status()
print(response)