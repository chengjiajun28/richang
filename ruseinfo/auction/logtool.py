import logging
import os
from logging.handlers import TimedRotatingFileHandler
import platform

plat = platform.system().lower()

# 日志打印格式
log_fmt = '%(asctime)s %(levelname)s: %(message)s'
formatter = logging.Formatter(log_fmt)

# 创建TimedRotatingFileHandler对象
logfile = "./log/tornadoapi.log"
if plat == 'linux':
    logfile = "/data/ruseinfo/log/fetchtask.log"
dirname = os.path.dirname(os.path.abspath(logfile))
os.makedirs(dirname, exist_ok=True)
log_file_handler = TimedRotatingFileHandler(filename=logfile, when="midnight", backupCount=30, encoding="utf-8")
log_file_handler.setFormatter(formatter)

# 设置日志记录级别为INFO
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.addHandler(log_file_handler)


def info(msg):
    log.info(msg)


def error(msg):
    log.error(msg)
