import requests
from datetime import timedelta


from estela_requests.middlewares.interface import EstelaMiddlewareInterface
from estela_requests.estela_hub import EstelaHub

RUNNING_STATUS = "RUNNING"
COMPLETED_STATUS = "COMPLETED"


class SpiderStatusMiddleware(EstelaMiddlewareInterface):

    def __init__(self, job, api_host, auth_token):
        self.api_host = api_host
        self.auth_token = auth_token
        job_jid, spider_sid, project_pid = job.split(".")
        self.job_url = f"{api_host}/api/projects/{project_pid}/spiders/{spider_sid}/job/{job_jid}"

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.job, estela_hub.api_host, estela_hub.auth_token)


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


    def before_session(self, *args, **kwargs):
        self.update_job(RUNNING_STATUS)

    def after_session(self, *args, **kwargs):
        self.update_job(COMPLETED_STATUS)
    
    def before_request(self, *args, **kwargs):
        pass

    def after_request(self, *args, **kwargs):
        pass