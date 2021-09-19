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


# @click.command()
# @click.option('-c', '--cfg_file', 'cfg_file', default='can_config.yml',
#               help='path to config file to use. Default is can_config.yml')
# @click.option('-l', '--logging_level', 'logging_level', default='INFO',
#               help='set logging severity DEBUG INFO WARNING ERROR CRITICAL.'+
#               'Default INFO')
# @click.option('-i', '--input', 'ifile_path', help='input file for parsing')
# @click.option('-o', '--output', 'ofile_path',
#               help='set generated file destination. Default ./')


def create_msg(frame_id,data_param):
    return can.Message(arbitration_id=frame_id, data=data_param)

print("Hello world")
db = cantools.database.load_file('./J1939-DBC/J1939_demo.dbc')

print("#### ")
msg_2182 = db.get_message_by_name('EEC1')

#print("printing msg 2192\n", msg_2182.signals)

can_bus = can.interface.Bus('can0', bustype='socketcan')

data_2182 = msg_2182.encode({'EngineSpeed':10.0})
msg_send = create_msg(msg_2182.frame_id,data_2182)
task_2182 = can_bus.send(msg_send)

#message = can_bus.recv()
#print("decoded msg:", db.decode_message(message.arbitration_id, message.data))

#print("checkpoint0", task_2182)

#message = can.Message(arbitration_id=example_message.frame_id, data=data)
#can_bus.send(message)
