"""Wrapper that allows to send requests in Estela platform and log them in the queue platform."""
import logging
from contextlib import contextmanager

from typing import Callable, Dict
from estela_requests.request_interfaces import HttpRequestInterface
from estela_requests.estela_http import EstelaResponse
from estela_requests.item_pipeline.manager import ItemPipelineManager
from estela_requests.item_pipeline.exporter import ItemExporterManager
from estela_requests.utils import get_estela_response
from estela_requests.estela_hub import EstelaHub
from estela_requests.middlewares.manager import MiddlewareManager

logger = logging.getLogger(__name__)

def apply_request_middlewares(func: Callable):
    def wrapper(wrapper_obj, *args, **kwargs) -> EstelaResponse:
        wrapper_obj.middleware_manager.apply_before_request_middlewares(*args, **kwargs)

        response = func(wrapper_obj, *args, **kwargs)
        estela_response = get_estela_response(response)

        wrapper_obj.middleware_manager.apply_after_request_middlewares(estela_response, *args, **kwargs)

        return response 

    return wrapper

class EstelaRequests:

    http_client: HttpRequestInterface
    def __init__(self, 
                 middleware_manager: MiddlewareManager,
                 item_pipeline_manager: ItemPipelineManager,
                 item_exporter_manager: ItemExporterManager,
                 http_client: HttpRequestInterface,
            ):
        self.middleware_manager = middleware_manager
        self.item_pipeline_manager = item_pipeline_manager
        self.item_exporter_manager = item_exporter_manager
        self.http_client = http_client
        self.middleware_manager.apply_before_session_middlewares()


    @classmethod
    @contextmanager
    def from_estela_hub(cls, estela_hub: EstelaHub):
        try:
            instance = cls(
                MiddlewareManager.from_estela_hub(estela_hub), ItemPipelineManager.from_estela_hub(estela_hub),
                ItemExporterManager.from_estela_hub(estela_hub), estela_hub.http_client, estela_hub,
            )
            yield instance
        except Exception:
            logger.exception("Exception while creating EstelaRequests instance using EstelaHub")
        finally:
            logger.debug("Cleaning up EstelaRequests...")
            logger.debug("Closing connection to the Estela platform")
            instance.cleanup_estela_requests()
            estela_hub.cleanup_resources()

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)
    
    def patch(self, *args, **kwargs):
        return self.request("PATCH", *args, **kwargs)
    
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
    
    def head(self, *args, **kwargs):
        return self.request("HEAD", *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)
    
    @apply_request_middlewares
    def request(self, *args, **kwargs):
        return self.http_client.request(*args, **kwargs)
    
    def send_item(self, item: Dict, *args, **kwargs):
        item = self.item_pipeline_manager.process_item(item)
        logger.debug("Exporting item: \n%s", item)
        self.item_exporter_manager.export_item(item)

    def free_resources(self):
        pass

    def cleanup_estela_requests(self):
        self.middleware_manager.apply_after_session_middlewares()
        self.free_resources()
