"""Middleware manager."""

from estela_requests.estela_hub import EstelaHub
from estela_requests.middlewares.interface import EstelaMiddlewareInterface


class MiddlewareManager:
    def __init__(self, middleware_list: list[EstelaMiddlewareInterface]) -> None:
        self.middleware_list = middleware_list

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        middleware_cls_list: list[type[EstelaMiddlewareInterface]] = estela_hub.middlewares
        middleware_list = []
        for middleware_cls in middleware_cls_list:
            middleware_list.append(middleware_cls.from_estela_hub(estela_hub))
        return cls(middleware_list)

    def prioritize_middlewares(self) -> None:
        pass

    def apply_before_request_middlewares(self, *args, **kwargs) -> None:
        for middleware in self.middleware_list:
            middleware.before_request(*args, **kwargs)

    def apply_after_request_middlewares(self, *args, **kwargs) -> None:
        for middleware in self.middleware_list:
            middleware.after_request(*args, **kwargs)

    def apply_before_session_middlewares(self, *args, **kwargs) -> None:
        for middleware in self.middleware_list:
            middleware.before_session(*args, **kwargs)

    def apply_after_session_middlewares(self, *args, **kwargs) -> None:
        for middleware in self.middleware_list:
            middleware.after_session(*args, **kwargs)
