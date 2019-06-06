#! encoding=utf-8

import logging
import time
import os

class MyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0):
        self.__timeformat__ = "%Y%m%d%H"
        self.rawFilename = filename
        self.latestTime = time.strftime(self.__timeformat__, time.localtime())
        self.filename = "%s.%s" % ( filename, self.latestTime )
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.baseFilename = os.path.abspath(self.filename)
        self.__createFile()
        super(MyFileHandler, self).__init__(self.rawFilename, mode, encoding, delay)
    def close(self):
        logging.FileHandler.close(self)
    def _open(self):
        return logging.FileHandler._open(self)
    def emit(self, record):
        currentTime = time.strftime(self.__timeformat__, time.localtime())
        if currentTime != self.latestTime:
            self.latestTime = currentTime
            self.filename = "%s.%s" % (self.rawFilename, self.latestTime)
            self.__createFile()
        logging.FileHandler.emit(self, record)
    def __createFile(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as fout:
                pass
        self.baseFilename = os.path.abspath(self.filename)
        if not os.path.exists(self.rawFilename):
            os.symlink(self.baseFilename, self.rawFilename)
        elif not os.path.islink(self.rawFilename):
            os.remove(self.rawFilename)
            os.symlink(self.baseFilename, self.rawFilename)
        elif os.path.realpath(self.rawFilename).split(".")[0] != self.filename.split(".")[0]:
            os.remove(self.rawFilename)
            os.symlink(self.baseFilename, self.rawFilename)
            self.stream = super(MyFileHandler, self)._open()

class Logger():
    def __init__(self, logname):
        '''
           指定保存日志的文件
           将日志存入到该文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        #fh = logging.FileHandler(logname)
        fh = MyFileHandler(logname)
        fh.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        string = '[%(levelname)s %(asctime)s %(process)d %(pathname)s:%(lineno)d %(funcName)s] %(message)s'
        formatter = logging.Formatter(string)
        fh.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
    def createLogger(self):
        return self.logger

def getLogger(logname):
    logger = Logger(logname)
    return logger.createLogger()

def testLogger1():
    logger.warning("ceshi")

def testLogger2():
    logger.warning("这是一个简单的测试")
    logger.warning("这是一个简单的测试")


if __name__ == "__main__":
    # 程序将会被记录在文件 testfile.log 中
    #logger = Logger(logname='testfile.log').createLogger()
    logger = getLogger("log/testfile.log")
    for i in range(180):
        testLogger1()
        testLogger2()
        time.sleep(1)
