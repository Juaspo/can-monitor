#!/usr/bin/env python3

# Script created to monitor canbus messages through picanDuo

__all__ = []
__version__ = "0.0.1"
__date__ = "2021-09-17"
__author__ = "Junior Asante"
__status__ = "development"


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
from pprint import pprint
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

@click.command()
@click.option('-c', '--cfg_file', 'cfg_file', default='can_config.yml',
              help='path to config file to use. Default is can_config.yml')
@click.option('-l', '--logging_level', 'logging_level', default='INFO',
              help='''set logging severity DEBUG INFO WARNING ERROR CRITICAL
              Default INFO''')
@click.option('-d', '--dbc', 'dbc_file', help='input .dbc file for encoding')
@click.option('-o', '--output', 'ofile_path',
              help='set generated file destination. Default ./')



def main(cfg_file: str, logging_level: str, dbc_file: str, ofile_path: str) -> int:
    logger = create_logger(logging_level)
    logger.info("Logging level set to: %s", logging_level)
    
    cfg_content = get_config(logger, cfg_file)

    if not cfg_content:
        logger.error("missing config file, exiting...")
        sys.exit(os.EX_CONFIG)

    print(cfg_content)

    return 0

def send_can():
    print("Hello world")
    db = cantools.database.load_file('./J1939-DBC/J1939_demo.dbc')

    print("#### ")
    msg_2182 = db.get_message_by_name('EEC1')

    #print("printing msg 2192\n", msg_2182.signals)

    can_bus = can.interface.Bus('can0', bustype='socketcan')

    data_2182 = msg_2182.encode({'EngineSpeed':10.0})
    msg_send = create_msg(msg_2182.frame_id,data_2182)
    task_2182 = can_bus.send(msg_send)

    return 0

def receive_can():
    message = can_bus.recv()
    print("decoded msg:", db.decode_message(message.arbitration_id, message.data))

    print("checkpoint0", task_2182)

    # message = can.Message(arbitration_id=example_message.frame_id, data=data)
    # can_bus.send(message)

def create_msg(frame_id,data_param):
    return can.Message(arbitration_id=frame_id, data=data_param)

def get_config(logger: Logger, cfg_file: str) -> dict:
    '''
    Fetch YAML configuration
    reads and returns YAML configuration
    input:
        cfg_file :str
    return:
        dict
    '''
    try:
        with open(cfg_file, 'r') as file:
            cfg = yaml.safe_load(file)
            logger.debug("yaml content: %s", cfg)
            return cfg["config_groups"]
    except yaml.YAMLError as e:
        logger.error(f"YAML file error: {e}")
    except FileNotFoundError as e:
        logger.error(f"config file error: {e}")
    return False

def create_logger(logging_level: str) -> Logger:
    '''
    Set up logger for this script
    input:
        logging_level :string
    return:
        logger :Logger
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, logging_level.upper(), 10))
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',  datefmt='%Y-%m-%d:%H:%M:%S')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    exit_code = 0
    #try:
    exit_code = main()
    #except Exception as e:
    #    print(f"Exiting with error {e}...", file=sys.stderr)
    sys.exit(exit_code)