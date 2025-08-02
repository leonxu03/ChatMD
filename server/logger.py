import logging

def setup_logger(name="Logger"):
    logger = logging.getLogger(name) # instantiate logger obj
    logger.setLevel(logging.DEBUG)

    # Print logs to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG) 

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] --- [%(message)s]")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger

logger = setup_logger()
logger.info("RAG process started")