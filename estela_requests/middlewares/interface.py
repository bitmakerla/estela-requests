"""Interface for middlewares."""

from abc import ABC, abstractmethod


class EstelaMiddlewareInterface(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def before_request(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_request(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def before_session(self, *args, **kwargs):
        pass
