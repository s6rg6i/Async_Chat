import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent / 'log_files/server.log'

# logger для клиента для стандартного потока вв и файлового
logger = logging.getLogger('server')  # регистратор с именем 'server'
logger.setLevel(logging.DEBUG)  # задаем уровень логирования DEBUG
# создаем файловый (уровень WARNING и ротацией в полночь) и консольный (уровень DEBUG) обработчик
fh = TimedRotatingFileHandler(FILE, encoding='utf-8', when="midnight", interval=1, backupCount=5)
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)  # для логирования в файл
ch.setLevel(logging.DEBUG)  # для консольного вывода при отладке
# создаем форматер и добавляем его в оба обработчика
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] -> %(message)s', '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)  # настроенные обработчики добавляем в 'logger'
logger.addHandler(ch)

# logger для декоратора для стандартного потока вв и файлового
decor_logger = logging.getLogger('client_decor')  # регистратор с именем 'client_decor'
decor_logger.setLevel(logging.DEBUG)  # задаем уровень логирования: DEBUG
dh = logging.FileHandler(FILE, encoding='utf-8')  # файловый обработчик
ch = logging.StreamHandler()  # консольный обработчик
dh.setFormatter(logging.Formatter("<%(asctime)s> %(message)s", '%Y-%m-%d %H:%M:%S'))
ch.setFormatter(logging.Formatter("%(message)s"))
decor_logger.addHandler(dh)  # настроенные обработчики добавляем в 'decor_logger'
decor_logger.addHandler(ch)


def log(f):
    def debug_log(*args, **kwargs):
        result = f(*args, **kwargs)
        # parent = inspect.stack()[1][3]  # другой вариант: имя родительской функции
        f_from = traceback.extract_stack()[-2]  # предпоследнюю запись
        decor_logger.debug(f'Function:[{f.__name__}({args},{kwargs})] File:[{f_from.filename}] '
                           f'line {f_from.lineno} from [{f_from.name}] [{f_from.line}]')
        return result

    return debug_log


if __name__ == '__main__':
    # проверка 1-го логгера
    logger.debug('debug сообщение')
    logger.info('info сообщение')
    logger.warning('warn сообщение')
    logger.error('error сообщение')
    logger.critical('debug сообщение')

    # проверка 2-го логгера
    @log
    def test(x, y):
        return x + y


    def parent_func():
        print(test(3, 5))


    parent_func()
