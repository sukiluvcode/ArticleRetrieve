"""
read configure file
"""
import os
import configparser

def get_config(config_name, section, option):
    """
    :param config_name: name of configure file
    :section: configure section
    :option: configure option
    """
    config_loc = os.path.split(__file__)[0]
    config_file = os.path.join(config_loc, config_name)
    
    config= configparser.ConfigParser()
    config.read(config_file)
    result = config.get(section=section, option=option)
    
    return result