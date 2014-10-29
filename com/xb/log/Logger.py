# coding:utf-8
'''
Created on 2014年9月5日

@author: kevin
'''
import os
import logging
import logging.config

print os.getcwd()

loggerFilePath = os.getcwd() + '\\conf\\logging.conf'
#print loggerFilePath
logging.config.fileConfig(loggerFilePath)

# create logger
logger = logging.getLogger("example01")


def printLogger(str):
    logger.info(str)
        
    
