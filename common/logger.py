#!/usr/bin/env python
# encoding: utf-8
import logging
import os
import time
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "log")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


class Logger(object):
    def __init__(self, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        log_file = time.strftime("%Y-%m-%d.log", time.localtime())
        path = os.path.join(LOG_DIR, log_file)
        self.logger = logging.getLogger(path)
        self.logger.setLevel(cmd_level)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        self.logger.addHandler(sh)

    def debug(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.debug(msg=unicode_msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.info(msg=unicode_msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.warn(msg=unicode_msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.error(msg=unicode_msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.critical(msg=unicode_msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        try:
            unicode_msg = msg.decode(encoding='utf-8', errors='ignore')
        except Exception:
            unicode_msg = msg
        self.logger.exception(msg=unicode_msg, *args, **kwargs)


logger = Logger()
LOG_DEBUG = logger.debug
LOG_INFO = logger.info
LOG_WARN = logger.warn
LOG_ERROR = logger.error
LOG_EXCEPTION = logger.exception
LOG_CRITICAL = logger.critical


def title(title):
    LOG_INFO("=" * 10)
    LOG_INFO(title)
    LOG_INFO("=" * 10)


def step(step):
    LOG_INFO("*" * 10)
    LOG_INFO(step)
    LOG_INFO("*" * 10)


TITLE = title
STEP = step


if __name__ == '__main__':
    LOG_DEBUG("DEBUG")
    LOG_INFO("INFO")
    LOG_ERROR("ERROR")
    LOG_EXCEPTION("EXCEPTION")
    LOG_CRITICAL("CRITICAL")

