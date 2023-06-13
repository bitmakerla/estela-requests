    # EstelaSDK tendria
    # producer, api_host, job, auth_token, http_client, args
import logging

from estela_queue_adapter.abc_producer import ProducerInterface
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
                 middlewares: list,
                 job_stats_topic: str,
                 job_requests_topic: str,
                 job_items_topic: str,
                 auth_token: str,
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
        self.auth_token = auth_token
        self.stats = {}

    def __repr__(self):
        attribute_str = '\n'.join([f"'{attr.upper()}': '{getattr(self, attr)}'" for attr in vars(self)])
        return f"EstelaHub(\n{{{attribute_str}}})"

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
                auth_token=settings.estela_auth_token,
            )
            logger.info("Estelahub: %s", estela_hub)
            return estela_hub
        except Exception as e:
            logger.exception("Failed to create EstelaHub from settings")
            raise e
