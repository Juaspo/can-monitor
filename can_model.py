#!/usr/bin/env python3
import re
import cantools
import can
import os.path
import logging

logger = logging.getLogger(__name__)

class CanApplication():
    def __init__(self, *args, **kwargs):
        self.canbus_port = None
        self.db = None
        self.can_interface = None
        self.callbacks = {}
        self.can_message_count = 0

    def reset_can_message_count(self):
        self.can_message_count = 0

    def add_can_message_count(self, n):
        self.can_message_count += n

    def set_can_channel(self, bus):
        self.canbus_port = str(bus)
        self.set_can_interface()

    def get_can_channel(self):
        return self.canbus_port

    def set_can_interface(self):
        self.can_interface = can.interface.Bus(str(self.canbus_port), bustype='socketcan')

    def get_can_interface(self):
        return self.can_interface

    def set_db(self, db_path):
        if(os.path.exists(db_path)):
            self.db = cantools.database.load_file(db_path)
            logger.debug("updated db with '%s'", db_path)
        else:
            logger.error("no db file found at '%s'", db_path)
            pass

    def send_can(self, arb_id: str, can_data: str):
        '''
        Send message on the canbus
        input:
            arb_id, data
        return:
            int
        '''
        # db = cantools.database.load_file('./J1939-DBC/J1939_demo.dbc')
        print("#### ")
        msg_2182 = self.db.get_message_by_name('EEC1')

        #print("printing msg 2192\n", msg_2182.signals)
        can_bus = self.get_can_interface()

        data_2182 = msg_2182.encode({'EngineSpeed':50.0})
        msg_send = self.create_msg(msg_2182.frame_id,data_2182)
        task_2182 = can_bus.send(msg_send)

        return 0

    def get_db_object(self, dbc_file_path: str):
        logger.debug(f"Using DBC file: %s", dbc_file_path)
        try:
            db = cantools.database.load_file(dbc_file_path)
            return db
        except FileNotFoundError as e:
            logger.error(f"DBC File not found: %s", e)
        return None


    def decode_can_msg(self, arb_id: str, can_data: str, db: object = None, dbc_file_path: str = None ) -> dict:
        if dbc_file_path is not None:
            db = get_db_object(dbc_file_path)   
        if db is None:
            raise ValueError ('Expected either db object or dbc_file path parameter')
            return None
        return db.decode_message(arb_id, can_data)


    def receive_can(self):
        can_bus = self.get_can_interface()
        if can_bus is None:
            logger.error("Can interface not setup")
            return None
        message = can_bus.recv()
        logger.info("Raw message received: %s", message)
        try:
            decoded_message = self.db.decode_message(message.arbitration_id, message.data)
            logger.info("msg id: [%s] msg data: [%s]", hex(message.arbitration_id), message.data)
            logger.info("decoded msg: %s", decoded_message)
        except KeyError as e:
            logger.warning("Did not find matching decoding parameter: %s", e)
        except ValueError as e:
            logger.warning("incorrect data received: %s", e)

        # delf.do_view_callback("receive_widget", message)

    def create_msg(self, frame_id, data_param):
        return can.Message(arbitration_id=frame_id, data=data_param)

    def add_view_callback(self, name, func):
        self.callbacks[name] = func

    def do_view_callback(self, name, data):
        if self.callbacks.get(name):
            self.callbacks[name]
            logger.debug("running %s callback method",  name)
        else:
            logger.warning("Callback method not found: %s", name)