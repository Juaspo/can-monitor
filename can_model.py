#!/usr/bin/env python3
import yaml

class ApplicationModel():
    def __init__(self, logger, *args, **kwargs):
        pass

    def get_config(self, logger, cfg_file: str) -> dict:
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

    def match_can_id(self, obj, can_id):
        pass


    def deep_search(self, obj, key):
        '''
        Search multiple levels of a dicts and return found key values

        input:
            obj: dict - Dictionary to search through
            key: str - Matching key string value to look for
        return:
            item: dict - Value of matching dict key
        '''

        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v,dict):
                item = self.deep_search(v, key)
                if item is not None:
                    return item


class CanApplication():
    def __init__(self, logger, *args, **kwargs):
        pass

    def test_function(self, logger, message):
        logger.info("Writing log with:%s", message)
        test_can = {"can_id": "001", "can_message": "0#00112233"}
        return test_can

    def send_can(self, arb_id: str, can_data: str):
        '''
        Send message on the canbus
        input:
            arb_id, data
        return:
            int
        '''
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

    def get_db_object(self, logger, dbc_file_path: str):
        logger.debug(f"Using DBC file: %s", dbc_file_path)
        try:
            db = cantools.database.load_file(dbc_file_path)
            return db
        except FileNotFoundError as e:
            logger.error(f"DBC File not found: %s", e)
        return None


    def decode_can_msg(self, logger, arb_id: str, can_data: str, db: object = None, dbc_file_path: str = None ) -> dict:
        if dbc_file_path is not None:
            db = get_db_object(logger, dbc_file_path)   
        if db is None:
            raise ValueError ('Expected either db object or dbc_file path parameter')
            return None
        return db.decode_message(arb_id, can_data)


    def receive_can(self):
        message = can_bus.recv()
        print("decoded msg:", db.decode_message(message.arbitration_id, message.data))
        print("checkpoint0", task_2182)

        # message = can.Message(arbitration_id=example_message.frame_id, data=data)
        # can_bus.send(message)

    def create_msg(self, frame_id, data_param):
        return can.Message(arbitration_id=frame_id, data=data_param)