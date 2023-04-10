## First draft version
from requests.sessions import Session

class RequestsWrapperSession(Session):
    def __init__(
        self,
        spider_name,
        spider_id,
        project_id="",
        job_id="",
    ) -> None:
        
        super().__init__()