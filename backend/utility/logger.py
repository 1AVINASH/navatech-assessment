import logging
import traceback

class LogLevels:
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG

class AppLogger:
    def __init__(self, name='app_logger', log_level=LogLevels.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): 
        self.logger.error(msg)
        self.logger.error(f"Traceback of the error {traceback.format_exc()}")

    def debug(self, msg): self.logger.debug(msg)

    def get_logger(self): return self.logger

app_logger = AppLogger().get_logger()