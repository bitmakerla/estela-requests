import logging
import sys
import time

from estela_queue_adapter.abc_producer import ProducerInterface

_stderr = sys.stderr


class KafkaLogHandler(logging.Handler):
    """Python kafka logging handler."""

    def __init__(self,
                level,
                producer: ProducerInterface,
                metadata: dict[str, str],
                topic: str,
        ) -> None:
        self.producer = producer
        self.metadata = metadata
        self.topic = topic
        super().__init__(level)


    @classmethod
    def from_estela_hub(cls, estela_hub):
        return cls(estela_hub.log_level, estela_hub.producer, {"jid": estela_hub.job}, estela_hub.job_logs_topic)

    def _logfn(self, message):
        data = {
            **self.metadata,
            "payload": {"log": str(message), "datetime": float(time.time())},
        }
        self.producer.send(self.topic, data)

    def emit(self, record):
        try:
            message = self.format(record)
            if message:
                self._logfn(message=message)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def handleError(self, record):  # noqa N802
        cur = sys.stderr
        try:
            sys.stderr = _stderr
        finally:
            super().handleError(record)
            sys.stderr = cur
