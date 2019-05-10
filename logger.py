#! encode=utf-8
import logging

class Logger():
    def __init__(self, logname):
        '''
           指定保存日志的文件路径
           将日志存入到该文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式，这是日志文件的行的格式
        string = '[%(levelname)s %(asctime)s %(process)d %(pathname)s:%(lineno)d %(funcName)s] %(message)s'
        formatter = logging.Formatter(string)
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    def createLogger(self):
        return self.logger

if __name__ == "__main__":
    # 程序将会被记录在文件 testfile.log 中
    logger = Logger(logname='testfile.log').createLogger()
    logger.warning("ceshi")
