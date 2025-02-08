import logging
import threading


class SingletonLogger:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_logger(cls, name='app_logger', log_file='app.log', level=logging.INFO) -> logging.Logger:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._setup_logger(name, log_file, level)
            return cls._instance

    @staticmethod
    def _setup_logger(name, log_file, level):
        print(f"Setting up logger {name} with log file {log_file} and level {level}")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger


# Create a global logger instance
logger = SingletonLogger.get_logger()
