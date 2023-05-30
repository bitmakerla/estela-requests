"""Request interfaces."""
import requests
from requests import PreparedRequest

class HttpRequestInterface:
    """It defines the expected interface that a request interface sholhd
    have to interact with estela wrapper"""
    def request(self, *args, **kwargs):
        pass
    
    def get(self, *args, **kwargs):
        pass

class RequestsInterface(HttpRequestInterface):
    prepared_request = None

    def request(self, *args, **kwargs):
        return requests.request(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)