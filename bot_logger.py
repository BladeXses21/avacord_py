import logging


def get_logger(name):
    logging.basicConfig(
        format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.FileHandler(f'bot.log', encoding='utf-8'), logging.StreamHandler()]
    )
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    return logger


andromeda_logger = get_logger('ANDROMEDA')
proxima_logger = get_logger('PROXIMA')
gluon_logger = get_logger('GLUON')
