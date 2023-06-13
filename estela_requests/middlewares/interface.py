"""Interface for middlewares."""

from abc import ABC, abstractmethod
from estela_requests.estela_hub import EstelaHub

class EstelaMiddlewareInterface(ABC):
    def __init__(self):
        pass

    # @abstractmethod
    # @classmethod
    # def from_estela_hub(cls, estela_hub: EstelaHub):
    #     pass

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
