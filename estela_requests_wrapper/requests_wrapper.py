## First draft version
import logging

from typing import Any, Optional, Union
from requests import Response, Session
#from estela_requests_wrapper.mixins import url_logger
from estela_queue_adapter import get_producer_interface

class EstelaRequestsWrapper:
    producer = get_producer_interface()
    #TODO anadir un handler que tenga soft y hard aviso cuando no esten
    # los parametros necesarios para subir el proyecto a estela.
    # project_id = 68b589b3-6b2c-4b39-beb8-1d45a496f6ef
    def __init__(self, spider_name: str) -> None:
        if self.producer.get_connection():
            print("Successful connection to the queue platform.")
        else:
            raise Exception("Could not connect to the queue platform.")
        self.spider_name = spider_name
        # Sacar el SID, JID y PID de las varibles y entorno.
        self.jid = "3.155.99b2627d-104f-425d-9158-d12fe8d1a245"
        super().__init__()
   
    # It could be seen as middleware
    # esto debe ser llamado desde el principio probablemente.
    # 
    def url_logger(self, func):
        def wrapper(*args, **kwargs):
            print(f"Realizando solicitud a: {args[2]}")
            response = func(*args, **kwargs)
            data = {
                "jid": self.jid,
                "payload": {
                    "url": response.url,
                    "status": int(response.status_code),
                    "method": response.request.method,
                    "duration": int(10),
                    "time": "time",
                    "response_size": len(response.content),
                    "fingerprint": "adsa",
                },
            }
            self.producer.send("job_requests", data)
            return response
        return wrapper
    
    def __del__(self):
        self.producer.flush()
        self.producer.close()


wrapper = EstelaRequestsWrapper("default")

class RequestsWrapperSession(Session):
    @wrapper.url_logger
    def request(self, method: str | bytes, url: str, *args, **kwargs) -> Response:
        return super().request(method, url, *args, **kwargs)
    
    def send_item(self, item):
        wrapper.producer.send("job_items", item)
        return item
