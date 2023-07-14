"""Handle EstelaRequests logs."""
import logging

from estela_queue_adapter import queue_noisy_libraries

from estela_requests.log_helpers.handlers import (
    KafkaLogHandler,  # TODO: make it more general, any handler
)


def init_logging(estela_hub, hdlr_flag, level=logging.DEBUG, noisy_log_libraries=[]):
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    for lib in noisy_log_libraries + queue_noisy_libraries:
        logging.getLogger(lib).addHandler(logging.NullHandler())
        logging.getLogger(lib).propagate = 0

    if hdlr_flag == 'kafka':
        hdlr = KafkaLogHandler.from_estela_hub(estela_hub)
    else:
        hdlr = logging.StreamHandler()
    hdlr.setLevel(level)
    hdlr.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
    root_logger.addHandler(hdlr)
