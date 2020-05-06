
"""
lesson 1 : example callback
"""

__all__ = [
    'myCallbackBrief', 
    'myCallback',
    ]

from ...session_logs import logger
logger.info(__file__)


def myCallbackBrief(key, doc):
    logger.info(key, len(doc))


def myCallback(key, doc):
    logger.info(key, len(doc))
    for k, v in doc.items():
        print("\t", k, v)
    logger.info("~~~~~~~~~~~~~~~~~~~~")
