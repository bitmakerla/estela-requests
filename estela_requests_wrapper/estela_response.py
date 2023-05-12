"""Class that the middlewares expect to receive."""

class EstelaRequest:
    def __init__(self, *args) -> None:
        pass

class EstelaResponse:
    def __init__(self, body: bytes, text: str, status_code, request: EstelaRequest, response_size, fingerprint, time_in_seconds) -> None:
        self.body = body
        self.text = text
        self.status_code = status_code
        self.request = request
        self.response_size = response_size
        self.fingerprint = fingerprint
        self.time_in_seconds = time_in_seconds