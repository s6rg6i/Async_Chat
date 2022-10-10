import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('server')  # регистратор с именем 'server'
logger.setLevel(logging.DEBUG)  # задаем уровень логирования DEBUG
# создаем файловый (уровень WARNING и ротацией в полночь) и консольный (уровень DEBUG) обработчик
fh = TimedRotatingFileHandler('log_files/server.log', encoding='utf-8', when="midnight", interval=1, backupCount=5)
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)  # для логирования в файл
ch.setLevel(logging.DEBUG)  # для консольного вывода при отладке
# создаем форматер и добавляем его в оба обработчика
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] -> %(message)s', '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)  # настроенные обработчики добавляем в 'logger'
logger.addHandler(ch)

if __name__ == '__main__':
    logger.debug('debug сообщение')
    logger.info('info сообщение')
    logger.warning('warn сообщение')
    logger.error('error сообщение')
    logger.critical('debug сообщение')
