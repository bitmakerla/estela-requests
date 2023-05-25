
def url_logger(func):
    """
    Decorator used to send requests info to the queue system.
    """
    def wrapper(self, method, url, *args, **kwargs):
        print(f"Realizando solicitud a: {url}")
        # data = {
        #     "jid": self.jid,
        #     "payload": {
        #         "url": response.url,
        #         "status": int(response.status),
        #         "method": request.method,
        #         "duration": int(request.meta.get("download_latency", 0) * 1000),
        #         "time": parse_time(),
        #         "response_size": len(response.body),
        #         "fingerprint": request_fingerprint(request),
        #     },
        # }
        # self.producer.send({"jid": self.jid, "payload": })
        return func(self, method, url, *args, **kwargs)
    return wrapper
