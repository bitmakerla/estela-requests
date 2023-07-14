"""Class that the middlewares expect to receive."""
class EstelaHttpRequest:
    def __init__(self, request_obj, *args) -> None:
        self.request_obj = request_obj

    @property
    def method(self):
        return self.request_obj.method


class EstelaResponse:
    def __init__(self,
                 url: str,
                 body: bytes,
                 text: str,
                 status_code: int,
                 request: EstelaHttpRequest,
                 response_size,
                 fingerprint,
                 time_in_seconds) -> None: # Add raw response
        self.url = url
        self.body = body
        self.text = text
        self.status_code = status_code
        self.request = request
        self.response_size = response_size
        self.fingerprint = fingerprint
        self.time_in_seconds = time_in_seconds
