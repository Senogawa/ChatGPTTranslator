import logging

logging.basicConfig(level = logging.INFO, format = "|%(levelname)s|-|%(process)s|-|%(asctime)s| %(message)s")
logger = logging.getLogger("Info")