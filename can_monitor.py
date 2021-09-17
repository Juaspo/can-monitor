__all__     = []
__version__ = 0.1
__date__    = "2021-09-17"
__author__  = "Junior Asante"
__status__  = "development"


import sys
import yaml
import click
import logging
from logging import Logger
import os
from datetime import datetime
import re
import cantools
import can

@click.command()
@click.option('-c', '--cfg_file', 'cfg_file', default='can_config.yml', help='path to config file to use. Default is can_config.yml')
@click.option('-l', '--logging_level', 'logging_level', default='INFO', help='set logging severity DEBUG INFO WARNING ERROR CRITICAL. Default INFO')
@click.option('-i', '--input', 'ifile_path', help='input file for parsing')
@click.option('-o', '--output', 'ofile_path', help='set generated file destination. Default ./')

print("Hello World")

