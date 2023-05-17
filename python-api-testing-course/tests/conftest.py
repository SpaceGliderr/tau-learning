import logging
import sys
import pytest

from reportportal_client import RPLogger, RPLogHandler


@pytest.fixture(scope="session")
def logger(request):
    # Create a logger instance from the logging package
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Check whether specific test node has particular config
    # If it does, attach a ReportPortal logger and handler classes
    if hasattr(request.node.config, "py_test_service"):
        # Creating ReportPortal logger and its handler class
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)

        # Add a console loggers
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        # If py_test_service not setup, then it just creates a normal StreamHandler and logger
        # StreamHandler listens to a stream of outputs and then sends it to the logger for logging
        rp_handler = logging.StreamHandler(sys.stdout)

    rp_handler.setLevel(logging.INFO)
    return logger
