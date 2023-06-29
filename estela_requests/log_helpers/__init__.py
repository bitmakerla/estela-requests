"""Handle EstelaRequests logs."""
import sys
import logging
from estela_requests.log_helpers.handlers import KafkaLogHandler  # TODO: make it more general, any handler

def init_logging(estela_hub, level=logging.DEBUG):
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    logging.getLogger('requests').setLevel(level)
    # logging.getLogger('urllib3').setLevel(logging.DEBUG)
    logging.getLogger('kafka').addHandler(logging.NullHandler())
    logging.getLogger('kafka').propagate = 0
    hdlr = KafkaLogHandler.from_estela_hub(estela_hub)
    #hdlr = logging.StreamHandler()
    hdlr.setLevel(level)
    hdlr.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
    root_logger.addHandler(hdlr)
