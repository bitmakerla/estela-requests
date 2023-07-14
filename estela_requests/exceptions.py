"""Exceptions for the estela_requests_wrapper package."""

class InvalidJobFormatError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class JobUpdateTimeoutError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
