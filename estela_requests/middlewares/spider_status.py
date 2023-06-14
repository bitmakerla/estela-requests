import requests
import logging
from datetime import timedelta
from typing import Dict


from estela_requests.middlewares.interface import EstelaMiddlewareInterface
from estela_requests.estela_hub import EstelaHub

logger = logging.getLogger(__name__)

RUNNING_STATUS = "RUNNING"
COMPLETED_STATUS = "COMPLETED"


class SpiderStatusMiddleware(EstelaMiddlewareInterface):

    def __init__(self, job, api_host, auth_token, stats: Dict = {}):
        self.api_host = api_host
        self.auth_token = auth_token
        job_jid, spider_sid, project_pid = job.split(".")
        self.job_url = f"{api_host}/api/projects/{project_pid}/spiders/{spider_sid}/jobs/{job_jid}"
        self.stats = stats

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.job, estela_hub.api_host, estela_hub.auth_token, estela_hub.stats)


    def update_job(
        self,
        status,
        lifespan=timedelta(seconds=0),
        total_bytes=0,
        item_count=0,
        request_count=0,
    ):
        res = requests.patch(
            self.job_url,
            data={
                "status": status,
                "lifespan": lifespan,
                "total_response_bytes": total_bytes,
                "item_count": item_count,
                "request_count": request_count,
            },
            headers={"Authorization": "Token {}".format(self.auth_token)},
        )
        if res.status_code != 200:
            logger.error("Failed to update job status, non-200 response")

    def before_session(self, *args, **kwargs):
        self.update_job(RUNNING_STATUS)

    def after_session(self, *args, **kwargs):
        self.update_job(
            COMPLETED_STATUS,
            lifespan=timedelta(seconds=self.stats.get("elapsed_time_seconds",0 )),
            item_count=self.stats.get("item_scraped_count", 0),
            total_bytes=self.stats.get("downloader/response_bytes", 0),
            request_count=self.stats.get("downloader/request_count", 0),
        )
    
    def before_request(self, *args, **kwargs):
        pass

    def after_request(self, *args, **kwargs):
        pass