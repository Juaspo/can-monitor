#!/usr/bin/env python3
import yaml
import logging
from logging import Logger
import sys
import os
import logging.config

logger = logging.getLogger(__name__)

class ApplicationUtils():
    def __init__(self, *args, **kwargs):
        pass

    def config_logger(self, logging_level: str, logging_cfg_path = None):
        '''
        Set up logger configuration either from yaml file
        or use default defined configuration below
        input:
            logging_level :string
        return:
            logger :Logger
        '''

        if (self.check_file(logging_cfg_path)):
            config = self.get_yaml_config(logging_cfg_path)
            logging.config.dictConfig(config)
        else:
            fmt = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
            date_fmt = "%y-%m-%d %H:%M:%S"

            logging.basicConfig(
                                level = str(logging_level),
                                format = fmt,
                                datefmt = date_fmt,
                                handlers = [
                                logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                                ])


    def check_file(self, file_path = None):
        if file_path is not None and os.path.exists(file_path):
            return file_path
        else:
            return None


    def get_yaml_config(self, cfg_file: str, return_top_level_cfg=None) -> dict:
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
                # logger.debug("yaml content: %s", cfg)
                if return_top_level_cfg is None:
                    return cfg
                elif cfg.get(return_top_level_cfg):
                    return cfg[return_top_level_cfg]
                else:
                    logger.warning("'%s' not found in top level yaml config", 
                                   return_top_level_cfg)
        except yaml.YAMLError as e:
            logger.error(f"YAML file error: {e}")
        except FileNotFoundError as e:
            logger.error(f"config file error: {e}")
        return False

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


    def byte_to_hex(self, byte_array, separator = ' '):
        logger.debug(byte_array)
        hex_result = " ".join(["{:02x}".format(x) for x in byte_array])
        return hex_result