"""Request interfaces."""
import requests

class HttpRequestInterface:
    """It defines the expected interface that a request interface sholhd
    have to interact with estela wrapper"""
    def request(self, *args, **kwargs):
        pass


class RequestsInterface(HttpRequestInterface):

    def request(self, *args, **kwargs):
        return requests.request(*args, **kwargs)
