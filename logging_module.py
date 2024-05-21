import logging
import sys
from logging.handlers import SysLogHandler


def logger_online():

    PAPERTRAIL_HOST = 'logs2.papertrailapp.com'
    PAPERTRAIL_PORT = 17832

    logger = logging.getLogger('pair_petro')
    logger.setLevel(logging.INFO)

    syslog = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))

    formatter = logging.Formatter('%(asctime)s - %(levelname)s[%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    syslog.setLevel(logging.INFO)
    syslog.setFormatter(formatter)

    logger.addHandler(syslog)

    return logger