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
        for mw in wrapper_obj.middleware_manager.middleware_list:
            mw.before_request(*args, **kwargs)

        response = func(wrapper_obj, *args, **kwargs)
        estela_response = get_estela_response(response)

        for mw in wrapper_obj.middleware_manager.middleware_list:
            mw.after_request(estela_response, *args, **kwargs)

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
                ItemExporterManager.from_estela_hub(estela_hub), estela_hub.http_client,
            )
            yield instance
        except Exception:
            logger.exception("Exception while creating EstelaRequests instance")
        finally:
            logger.debug("Closing connection to the Estela platform")
            instance.cleanup_estela_requests()

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)
    
    def patch(self, *args, **kwargs):
        return self.request("PATCH", *args, **kwargs)
    
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
    
    @apply_request_middlewares
    def request(self, *args, **kwargs):
        return self.http_client.request(*args, **kwargs)
    
    def send_item(self, item: Dict, *args, **kwargs):
        item = self.item_pipeline_manager.process_item(item)
        logger.debug("Exporting item: \n%s", item)
        self.item_exporter_manager.export_item(item)

    def call_after_session_middlewares(self):
        self.middleware_manager.apply_after_session_middlewares()

    def free_resources(self):
        from estela_requests.config import settings
        settings.estela_producer.flush()
        settings.estela_producer.close()  #TODO: donde se deberia hacer esto?, en cada clase?

    def cleanup_estela_requests(self):
        self.middleware_manager.apply_after_session_middlewares()
        self.free_resources()


# EstelaSDK tendria
# producer, api_host, job, auth_token, http_client, args

# Settings.py se veria como
# middlewares = RequestsHistry, Stats, Status
# producer = self.get_producer()
# job = os.getenv(JOB, "")
# api_host = os.get()
# auth_token = os.get(auth_toekn)
# http_client = self.get_clinet()
# args = self.getenv(args, "")
# middlewares = [
#   "path_al_middleware",
#   "path_al_middleware_2",
# ]
# 
# Responsabilities
# estela_medium
# estela_sdk tendria todos los attr relevantes para poder comunicarse con estela, se construye desde los settings
# Pruebas para estela_sdk: ver que tenga todos los atributos y se pueda construir de diferentes maneras.
# middleware_manager necesita el estela_sdk y middleware_list o se puede construir desde los settings tambien.
# Pruebsa para middleware manager, que ejecute los middlewares en el orden correspodiente
# Que se construya de las maneras adecuadas
# EstelaWrapper sera usada por el usuario y deberia ser manejada de la misma manera que requests,
# es decir no deberia necesitar ni un solo argumento.
# EstelaWrapper necesita un estela_medium y middlewares que seran corridos, ambos se pueden obtener el entorno,
# settings.py
# EstelaWrapper se encarga de ejecutar el workflow.
# Este workflow consiste en ejecutar los middlewares a su debido tiempo.
# Pruebas para EstelaWrapper seria ver que los middlewares son ejecutados y modifican lo que se obtenga
# como respuesta.
