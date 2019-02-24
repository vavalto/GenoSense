import logging
import logging.handlers

LOG_FILE_DIRECTORY = r'./logs/'

LOGGING_LEVELS = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARN': logging.WARN,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}


def create_logger(name=None, logging_configuration=None):
    if not logging_configuration:
        return None
    logging.basicConfig(level=LOGGING_LEVELS[logging_configuration["level"]])
    logger = logging.getLogger(name)
    file_handler = logging.handlers.RotatingFileHandler(filename=f'{LOG_FILE_DIRECTORY}{name}.log',
                                                        maxBytes=logging_configuration["log_file_size"],
                                                        backupCount=logging_configuration["log_file_rollover_count"])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
