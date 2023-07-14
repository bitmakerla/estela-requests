    # EstelaSDK tendria
    # producer, api_host, job, auth_token, http_client, args
import logging

from estela_queue_adapter.abc_producer import ProducerInterface

from estela_requests.item_pipeline import ItemPipelineInterface
from estela_requests.item_pipeline.exporter import ItemExporterInterface
from estela_requests.log_helpers import init_logging
from estela_requests.middlewares.interface import EstelaMiddlewareInterface
from estela_requests.request_interfaces import HttpRequestInterface

logger = logging.getLogger(__name__)

class EstelaHub:
    """Class that should contain all the necessary information to communicate with Estela.

    We need to communicate with the queue platform and the API.
    """

    def __init__(self,
                 producer: ProducerInterface,
                 api_host: str,
                 job: str,
                 http_client: HttpRequestInterface,
                 args: str,
                 middlewares: list[EstelaMiddlewareInterface],
                 job_stats_topic: str,
                 job_requests_topic: str,
                 job_items_topic: str,
                 job_logs_topic: str,
                 auth_token: str,
                 item_pipelines: list[ItemPipelineInterface],
                 item_exporters: list[ItemExporterInterface],
                 log_level: int,
                 log_flag: str,
                 log_libraries: list[str],
                 ) -> None:
        self.producer = producer
        self.api_host = api_host
        self.job = job
        self.http_client = http_client
        self.args = args
        self.middlewares = middlewares
        self.job_stats_topic = job_stats_topic
        self.job_requests_topic = job_requests_topic
        self.job_items_topic = job_items_topic
        self.job_logs_topic = job_logs_topic
        self.auth_token = auth_token
        self.stats = {}
        self.item_pipelines = item_pipelines
        self.item_exporters = item_exporters
        self.log_level = logging._levelToName.get(log_level, "UNKNOWN")
        self.log_flag = log_flag
        self.log_libraries = log_libraries

    def __repr__(self) -> str:
        attribute_str = '\n '.join([f"'{attr.upper()}': '{getattr(self, attr)}'," for attr in vars(self)])
        return f"EstelaHub(\n{{{attribute_str}\n}})"

    def cleanup_resources(self):
        """Cleanup resources."""
        if self.producer:
            self.producer.flush()
            self.producer.close()

    @classmethod
    def create_from_settings(cls):
        try:
            from estela_requests.config import settings
            estela_hub = cls(
                producer=settings.estela_producer,
                api_host=settings.estela_api_host,
                job=settings.estela_spider_job,
                http_client=settings.http_client,
                args=settings.estela_spider_args,
                middlewares=settings.estela_middlewares,
                job_stats_topic=settings.job_stats_topic,
                job_requests_topic=settings.job_requests_topic,
                job_items_topic=settings.job_items_topic,
                job_logs_topic=settings.job_logs_topic,
                auth_token=settings.estela_auth_token,
                item_pipelines=settings.estela_item_pipelines,
                item_exporters=settings.estela_item_exporters,
                log_level=settings.estela_log_level,
                log_flag=settings.estela_log_flag,
                log_libraries=settings.estela_noisy_libraries,
            )
            init_logging(estela_hub, settings.estela_log_flag, settings.estela_log_level, settings.estela_noisy_libraries)
            logger.debug("Estela Hub Created from settings: %s", estela_hub)
            return estela_hub
        except Exception as e:
            logger.exception("Failed to create EstelaHub from settings")
            raise e
