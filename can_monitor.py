#!/usr/bin/env python3

# Script created to monitor canbus messages through picanDuo

__all__ = []
__version__ = "0.0.1"
__date__ = "2021-09-17"
__author__ = "Junior Asante"
__status__ = "development"


import sys
import click
import os
import tkinter as tk
import threading
import logging
import can_m_gui
import can_model
import utils



@click.command()
@click.option('-c', '--cfg_file', 'cfg_file', default='can_config.yml',
              help='path to config file to use. Default is can_config.yml')
@click.option('-l', '--logging_level', 'logging_level', default='DEBUG',
              help='''set logging severity DEBUG INFO WARNING ERROR CRITICAL
              Default INFO''')
@click.option('-L', '--logging_cfg', 'logging_config',
              help='''Use logging yaml config file to set logging configuration''')
@click.option('-d', '--dbc', 'dbc_file', help='input .dbc file for encoding')
@click.option('-o', '--output', 'ofile_path',
              help='set generated file destination. Default ./')


def main(cfg_file: str, logging_level: str, logging_config:str, dbc_file: str, 
         ofile_path: str) -> int:
    util = utils.ApplicationUtils()
    util.config_logger(logging_level, logging_config)

    logger = logging.getLogger(__name__)
    logger.info("Logging level set to: %s", logging_level)

    root = tk.Tk()
    root.withdraw()

    can_controller = CanController(root, logger, cfg_file) 
    root.mainloop()
    return 0

class CanController(utils.ApplicationUtils):
    def __init__(self, root, logger, cfg_file, *arg, **kwargs):
        data_val = {"can_data": "New value!", "can_info": "new info!"}
        self.logger = logger
        self.threads = {}

        self.can_control = can_model.CanApplication(self)
        self.can_control.set_can_channel("can0")

        cfg_content = {"can_data": "New value!", "can_info": "new info!"}
        cfg_content = self.get_yaml_config(cfg_file)
        if not cfg_content:
            logger.error("missing config file, exiting...")
            sys.exit(os.EX_CONFIG)

        dbc_path = self.get_yaml_config(cfg_file, "dbc_file")
        if dbc_path:
           self.can_control.set_db(dbc_path)

        can_receive_cfg = self.deep_search(cfg_content, "can_receive")
        logger.debug("receive cfg_file content:\n%s", can_receive_cfg)

        self.can_gui = can_m_gui.MainApplication(root, can_receive_cfg)
        self.can_gui.add_callback("exit", self.on_exit)

        widgets = self.can_gui.receive_widgets
        start_page = self.can_gui.pages["StartPage"]

        start_page.btn0.config(command = lambda: self.can_control.send_can("123", "998877"))
        start_page.btn1.config(command = lambda: self.start_thread("CanMonitorThread"))
        start_page.btn2.config(command = lambda: self.can_read_stop())

    def start_thread(self, thread_name):
        create_new_thread = True

        if self.threads.get(thread_name):
            if self.threads[thread_name].isAlive():
                create_new_thread = False
                self.logger.info("%s thread is already running", thread_name)
                # return threads[thread_name]

        if create_new_thread:
            x_thread = threading.Thread(target=self.can_read, args=(thread_name,))
            x_thread.start()
            self.threads[thread_name] = x_thread
            self.logger.info("New thread '%s' created and started", thread_name)
            # return x_thread

    def can_read(self, name):
        self.logger.info("%s is running can monitor", name)
        self.can_control.receive_can()

    def can_read_stop(self):
        self.can_control.stop_receive_can()
        self.logger.info("Stopped can receive can")

    def update_widget(self, widget_name, data):

        widgets[widget_name].update_values(logger, data_val)

    def fetch_entry_data(self):
        entry_data = None
        page = self.can_gui.pages["StartPage"]
        entry_data = page.get_entry_data()
        logger.info(entry_data)

    def on_exit(self):
        self.can_read_stop()
        self.logger.debug("closing application")




if __name__ == "__main__":
    exit_code = 0
    #try:
    exit_code = main()
    #except Exception as e:
    #    print(f"Exiting with error {e}...", file=sys.stderr)
    sys.exit(exit_code)
