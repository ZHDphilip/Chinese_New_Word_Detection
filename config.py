# -*- coding: utf-8 -*-
"""
# © 07/20/2020 by ZihaoDONG, ALL RIGHTS RESERVED
# File name: config.py
# This project is an upgrade version of @zhanzecheng's Project
# Replaced list with dict, significantly boosting searching and insertion time
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    REQUEST_STATS_WINDOW = 15


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
