import logging

logger = logging.getLogger('client')  # регистратор с именем 'client'
logger.setLevel(logging.DEBUG)  # задаем уровень логирования: DEBUG
# создаем файловый (уровень WARNING) и консольный (уровень DEBUG) обработчик
fh, ch = logging.FileHandler('log_files/client.log', encoding='utf-8'), logging.StreamHandler()
fh.setLevel(logging.DEBUG)  # для логирования в файл
ch.setLevel(logging.DEBUG)  # для консольного вывода при отладке
# создаем форматер и добавляем его в оба обработчика
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] [%(module)s] -> %(message)s', '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)  # настроенные обработчики добавляем в 'logger'
logger.addHandler(ch)

if __name__ == '__main__':
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
