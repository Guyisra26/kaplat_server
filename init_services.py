from logging_config import create_logger
import logging

# Global request counter (dictionary to allow mutation inside middleware)
request_counter = {"count": 0}

# Loggers
request_logger = create_logger(
    name="request-logger",
    filename="requests.log",
    level=logging.INFO,
    to_stdout=True
)

stack_logger = create_logger(
    name="stack-logger",
    filename="stack.log",
    level=logging.INFO
)

independent_logger = create_logger(
    name="independent-logger",
    filename="independent.log",
    level=logging.DEBUG
)
