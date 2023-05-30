"""Exceptions for the estela_requests_wrapper package."""

class UnexpectedResponseType(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
