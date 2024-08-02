import logging
import os
import colorlog
from logging.handlers import RotatingFileHandler
from datetime import datetime

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

default_formats = {
    # 终端输出格式
    'console_format': '%(log_color)s%(levelname)s: %(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s',
    # 日志输出格式
    'log_format': '%(levelname)s:%(asctime)s-%(filename)s-[line:%(lineno)d]- %(message)s'
}


class Logger:
    """
    1. 创建日志记录器logging.getLogger
    2. 设置日志级别logger.setLevel
    3. 创建日志文件logging.FileHandler
    4. 设置日志格式logging.Formatter
    5. 将日志处理程序记录到记录器addHandler
    """

    def __init__(self, file_path, level: int | str = logging.DEBUG):
        # 需要打日志的文件路径
        cur_path = os.path.dirname(file_path)
        # 去掉后缀的文件名
        file_name_only = os.path.splitext(os.path.basename(file_path))[0]

        # 日志文件夹名称
        log_path = os.path.join(cur_path, 'logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        # 当前时间，格式化为"年-月-日"
        self.__now_time = datetime.now().strftime('%Y-%m-%d')
        # 打印所有信息的日志路径，eg:"logger\log\logger_all.log"
        self.__all_log_path = os.path.join(log_path, file_name_only + "_all" + ".log")
        # 仅打印错误信息的日志路径
        self.__error_log_path = os.path.join(log_path, file_name_only + "_error" + ".log")
        # 创建日志记录器
        self.__logger = logging.getLogger(file_name_only)
        # 设置默认日志记录器记录级别
        self.__logger.setLevel(level)

        self.__setup_handlers()

    def __setup_handlers(self):
        # 先生成三个Handler
        all_logger_handler = self.__init_logger_handler(self.__all_log_path)
        error_logger_handler = self.__init_logger_handler(self.__error_log_path)
        console_handler = self.__init_console_handler()

        # 设置三个Handler的格式
        self.__set_log_formatter(all_logger_handler)
        self.__set_log_formatter(error_logger_handler)
        self.__set_console_formatter(console_handler, log_colors_config)

        # 设置三个Handler的
        self.__set_log_handler(all_logger_handler)
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)
        self.__set_console_handler(console_handler)

    @staticmethod
    def __init_logger_handler(log_path):
        """
               创建日志记录器handler，用于收集日志
               :param log_path: 日志文件路径
               :return: 日志记录器
               """
        # 写入文件，如果文件超过1M大小时，切割日志文件，仅保留3个文件
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=1 * 1024 * 1024, backupCount=3,
                                             encoding='utf-8')
        return logger_handler

    @staticmethod
    def __init_console_handler():
        """创建终端日志记录器handler，用于输出到控制台"""
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __set_log_handler(self, logger_handler, level: int | str = logging.DEBUG):
        """
               设置handler级别并添加到logger收集器
               :param logger_handler: 日志记录器
               :param level: 日志记录器级别
               """
        logger_handler.setLevel(level)
        self.__logger.addHandler(logger_handler)

    def __set_console_handler(self, console_handler):
        """
                设置handler级别并添加到终端logger收集器
                :param console_handler: 终端日志记录器
                :param level: 日志记录器级别
                """
        console_handler.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handler)

    @staticmethod
    def __set_console_formatter(console_handler, color_config):
        """
               设置输出格式-控制台
               :param console_handler: 终端日志记录器
               :param color_config: 控制台打印颜色配置信息
               :return:
               """
        formatter = colorlog.ColoredFormatter(default_formats["console_format"], log_colors=color_config)
        console_handler.setFormatter(formatter)

    @staticmethod
    def __set_log_formatter(file_handler):
        """
           设置日志输出格式-日志文件
           :param file_handler: 日志记录器
        """
        formatter = logging.Formatter(default_formats["log_format"], datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    """
    stacklevel 参数设置为 3（对于这种情况下的标准调用）。
    这个设置会告诉 logging 模块，跳过当前函数和调用它的函数的堆栈帧，以获取实际调用 Logger 实例方法的堆栈帧信息
    """

    def __console(self, level, message):
        if level == 'info':
            self.__logger.info(message, stacklevel=3)
        elif level == 'debug':
            self.__logger.debug(message, stacklevel=3)
        elif level == 'warning':
            self.__logger.warning(message, stacklevel=3)
        elif level == 'error':
            self.__logger.error(message, stacklevel=3)
        elif level == 'critical':
            self.__logger.critical(message, stacklevel=3)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def critical(self, message):
        self.__console('critical', message)


if __name__ == '__main__':
    log = Logger(__file__)

    log.info("这是日志信息")
    log.debug("这是debug信息")
    log.warning("这是警告信息")
    log.error("这是错误日志信息")
    log.critical("这是严重级别信息")
