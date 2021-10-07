#!/usr/bin/env python3

# Script created to monitor canbus messages through picanDuo

__all__ = []
__version__ = "0.0.1"
__date__ = "2021-09-17"
__author__ = "Junior Asante"
__status__ = "development"


import sys
# import yaml
import click
import logging
from logging import Logger
import os
from datetime import datetime
import re
import cantools
import can
from pprint import pprint
import tkinter as tk
# from tkinter import *
# from tkinter import messagebox
# from tkinter import ttk
import can_m_gui
import can_model


@click.command()
@click.option('-c', '--cfg_file', 'cfg_file', default='can_config.yml',
              help='path to config file to use. Default is can_config.yml')
@click.option('-l', '--logging_level', 'logging_level', default='DEBUG',
              help='''set logging severity DEBUG INFO WARNING ERROR CRITICAL
              Default INFO''')
@click.option('-d', '--dbc', 'dbc_file', help='input .dbc file for encoding')
@click.option('-o', '--output', 'ofile_path',
              help='set generated file destination. Default ./')


def main(cfg_file: str, logging_level: str, dbc_file: str, ofile_path: str) -> int:
    logger = create_logger(logging_level)
    logger.info("Logging level set to: %s", logging_level)

    root = tk.Tk()
    root.withdraw()
    can_controller = CanController(root, logger, cfg_file)
    # can_gui.receive_widgets["widdy1"].update_label("canaddr", "sub", data_val)

    root.mainloop()
    return 0


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
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                  datefmt='%Y-%m-%d:%H:%M:%S')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

class CanController():
    def __init__(self, root, logger, cfg_file, *arg, **kwargs):
        self.app_model = can_model.ApplicationModel(self, logger)
        self.can_control = can_model.CanApplication(self, logger)
        # can_controller = CanController(self, logger)

        cfg_content = self.app_model.get_config(logger, cfg_file)

        if not cfg_content:
            logger.error("missing config file, exiting...")
            sys.exit(os.EX_CONFIG)

        can_receive_cfg = self.app_model.deep_search(cfg_content, "can_receive")
        logger.debug("receive cfg_file content:\n%s", can_receive_cfg)

        self.can_gui = can_m_gui.MainApplication(root, logger, can_receive_cfg)

        data_val = {"can_data": "New value!", "can_info": "new info!"}
        # self.can_gui.receive_widgets["engine_speed"].update_values(data_val)
        # can_gui.destroy()

        widgets = self.can_gui.receive_widgets

        start_page = self.can_gui.pages["StartPage"]
        # start_page.set_entry("potato")
        # print(start_page)
        # print(widgets)
        
        widgets["engine_speed"].update_values(logger, data_val)

        # data_val = {"address": "7AF#", "value": "Success! New value"}

    def fetch_entry_data(self, logger):
        entry_data = None
        page = self.can_gui.pages["StartPage"]
        entry_data = page.get_entry_data()
        logger.info(entry_data)

    # def update_widget(logger):


if __name__ == "__main__":
    exit_code = 0
    #try:
    exit_code = main()
    #except Exception as e:
    #    print(f"Exiting with error {e}...", file=sys.stderr)
    sys.exit(exit_code)
