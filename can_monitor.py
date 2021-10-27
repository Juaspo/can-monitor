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
@click.option('-D', '--dbc', 'dbc_file', help='input .dbc file for encoding')
@click.option('-d', '--dry', 'dry_run', is_flag=True, default=False, 
              help='input .dbc file for encoding')
@click.option('-o', '--output', 'ofile_path',
              help='set generated file destination. Default ./')


def main(cfg_file: str, logging_level: str, logging_config:str, dbc_file: str, 
         dry_run: bool, ofile_path: str) -> int:
    util = utils.ApplicationUtils()
    util.config_logger(logging_level, logging_config)

    logger = logging.getLogger(__name__)
    logger.info("Logging level set to: %s", logging_level)

    if dry_run:
        logger.info("Dry run mode. No active connection will be attempted")

    root = tk.Tk()
    root.withdraw()

    can_controller = CanController(root, logger, cfg_file, **({"dry": dry_run})) 
    root.mainloop()
    return 0

class CanController(utils.ApplicationUtils):
    def __init__(self, root, logger, cfg_file, *arg, **kwargs):
        data_val = {"can_data": "New value!", "can_info": "new info!"}
        self.dry_run = False

        self.dry_run = kwargs.get("dry", False)
        logger.info("Dry mode: %s", self.dry_run)

        self.logger = logger
        self.threads = {}

        self.can_control = can_model.CanApplication(self, **({"dry": self.dry_run}))
        self.can_control.set_can_channel("can0")
        self.can_control.add_callback("update_receive_widget_view", self.update_receive_widget_view)
        self.can_control.add_callback("update_send_widget_view", self.update_send_widget_view)

        cfg_content = {"can_data": "New value!", "can_info": "new info!"}
        cfg_content = self.get_yaml_config(cfg_file)
        if not cfg_content:
            logger.error("missing config file, exiting...")
            sys.exit(os.EX_CONFIG)

        dbc_path = self.get_yaml_config(cfg_file, "dbc_file")
        if dbc_path:
           self.can_control.set_db(dbc_path)

        self.can_widget_cfg = self.deep_search(cfg_content, "can_widget_parameters")
        logger.debug("receive cfg_file content:\n%s", self.can_widget_cfg)

        self.can_gui = can_m_gui.MainApplication(root, self.can_widget_cfg)
        self.can_gui.add_callback("exit", self.on_exit)

        self.receive_widgets = self.can_gui.receive_widgets
        self.send_widgets = self.can_gui.send_widgets
        start_page = self.can_gui.pages["StartPage"]

        start_page.btn0.config(command = lambda: self.can_control.send_can("123", "998877"))
        start_page.btn1.config(command = lambda: self.start_thread("CanMonitorThread"))
        start_page.btn2.config(command = lambda: self.can_read_stop())
        start_page.check0.config(command = lambda: self.prep_can_filter(start_page.filter_check.get()))

        self.get_can_info_from_dbc()


    def start_thread(self, thread_name):
        '''
        Thread starter function.

        '''

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
        '''
        Function to initiate CAN buffer read to see if any incoming
        CAN messages exist
        '''
        self.logger.info("%s is running can monitor", name)
        self.can_control.receive_can()

    def can_read_stop(self):
        '''
        Trigger to stop CAN read loop gracefully
        '''

        self.can_control.stop_receive_can()
        self.logger.info("Stopped can receive can")

    def get_can_info_from_dbc(self):
        '''
        Fetch CAN info from DBC file if 'get_can_info' is True
        '''

        for widget_type in self.can_widget_cfg:
            for widget in self.can_widget_cfg[widget_type]:
                self.logger.info("current widget %s - %s", widget_type, widget)
                if self.can_widget_cfg[widget_type][widget].get("get_can_info", False):
                    result = self.can_control.get_can_by_name(widget)
                    self.logger.debug(result)
                    if result is not None:
                        result["can_id"] = hex(result["can_id"]).upper()
                        self.update_send_widget_view(result)


    def prep_can_filter(self, set_filter):
        '''
        Prepare and set up can filters
        '''
        filter_list = []
        filter_dict = {}
        if set_filter:
            for can_id in self.receive_widgets:
                filter_dict["can_id"] = can_id
                filter_dict["can_mask"] = 255
                # filter_dict["extended"] = False
            filter_list.append(filter_dict)
            self.logger.info("widgets: %s", filter_list)
            self.can_control.set_can_filters(filter_list)
        else:
            self.can_control.set_can_filters(False)

        self.logger.info("Set can filter %s", set_filter)

    def update_receive_widget_view(self, data):
        '''
        Function to update "Receive widget fields"
        '''

        # self.logger.debug(data)
        new_dict = {}
        # TODO requires python 3.8 for optional arg in hex()
        # proper_hex = data["can_data"].hex(' ').upper()

        if self.receive_widgets.get(data["can_id"]):
            self.logger.info("Found can id match: %s", data["can_id"])
            proper_hex = self.byte_to_hex(data["can_data"])


            new_dict["can_data"] = proper_hex.upper()
            if data.get("decoded"):
                for k, v in data["decoded"].items():
                    new_dict["can_name"] = k
                    new_dict["can_value"] = v

            self.logger.debug("Received can %s", new_dict)
            self.recieve_widgets[data["can_id"]].update_values(new_dict)


    def update_send_widget_view(self, data):
        '''
        Function to update "Send widget fields"
        '''
        if data.get("can_name"):
            canname = data["can_name"]
            self.send_widgets[canname].update_values(data)
            self.logger.info(data)
        else:
            self.logger.warning("No 'can_name' provided: %s", data)

    #     # self.logger.debug(data)
    #     new_dict = {}
    #     # TODO requires python 3.8 for optional arg in hex()
    #     # proper_hex = data["can_data"].hex(' ').upper()

    #     if self.send_widgets.get(data["can_id"]):
    #         self.logger.info("Found can id match: %s", data["can_id"])
    #         proper_hex = self.byte_to_hex(data["can_data"])


    #         new_dict["can_data"] = proper_hex.upper()
    #         if data.get("decoded"):
    #             for k, v in data["decoded"].items():
    #                 new_dict["can_name"] = k
    #                 new_dict["can_value"] = v

    #         self.logger.debug("Received can %s", new_dict)
    #         self.send_widgets[data["can_id"]].update_values(new_dict)


    def fetch_entry_data(self):
        entry_data = None
        page = self.can_gui.pages["StartPage"]
        entry_data = page.get_entry_data()
        logger.info(entry_data)

    def on_exit(self):
        '''
        Function to shut down application gracefully.
        This function will allow looped threads to quit and shut down
        properly before application quites
        '''
        self.can_read_stop()
        self.logger.debug("closing application")

    # def get_name_from_id(self, cfg_file, arb_id):

    #     cfg_file = self.deep_search(cfg_file, "can_widget_parameters")
    #     for entry in cfg_file

    # def get_id_dict(self, cfg_file, data):
    #     can_id = None
    #     new_dict = {}
    #     sub_dict = {}

    #     for entry in cfg_content:
    #         can_id = cfg_file[entry]["can_id"]
    #         for item in cfg_file[entry]:
    #             sub_dict[item]




if __name__ == "__main__":
    exit_code = 0
    #try:
    exit_code = main()
    #except Exception as e:
    #    print(f"Exiting with error {e}...", file=sys.stderr)
    sys.exit(exit_code)
