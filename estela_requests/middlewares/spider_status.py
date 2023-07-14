import logging
from datetime import timedelta

import requests

from estela_requests.estela_hub import EstelaHub
from estela_requests.exceptions import InvalidJobFormatError, JobUpdateTimeoutError
from estela_requests.middlewares.interface import EstelaMiddlewareInterface

logger = logging.getLogger(__name__)

RUNNING_STATUS = "RUNNING"
COMPLETED_STATUS = "COMPLETED"


class SpiderStatusMiddleware(EstelaMiddlewareInterface):

    def __init__(self, job, api_host, auth_token, stats: dict = {}) -> None:
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
        if status not in [RUNNING_STATUS, COMPLETED_STATUS]:
            raise InvalidJobFormatError("Invalid job status")
        if not isinstance(lifespan, timedelta):
            raise InvalidJobFormatError("Invalid lifespan")
        try:
            res = requests.patch(
                self.job_url,
                data={
                    "status": status,
                    "lifespan": lifespan,
                    "total_response_bytes": total_bytes,
                    "item_count": item_count,
                    "request_count": request_count,
                },
                headers={"Authorization": f"Token {self.auth_token}"},
                timeout=20,
            )
            if res.status_code != 200:
                logger.error("Failed to update job status, non-200 response")
        except requests.exceptions.Timeout:
            raise JobUpdateTimeoutError("Update job status takes too long.")


    def before_session(self, *args, **kwargs):
        self.update_job(RUNNING_STATUS)

    def after_session(self, *args, **kwargs):
        self.update_job(
            COMPLETED_STATUS,
            lifespan=timedelta(seconds=self.stats.get("elapsed_time_seconds", 0)),
            item_count=self.stats.get("item_scraped_count", 0),
            total_bytes=self.stats.get("downloader/response_bytes", 0),
            request_count=self.stats.get("downloader/request_count", 0),
        )

    def before_request(self, *args, **kwargs):
        pass

    def after_request(self, *args, **kwargs):
        pass
