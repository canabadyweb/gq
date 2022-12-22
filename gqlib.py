import os
import configparser

user_config_dir = os.path.expanduser("~") + "/.config/gq"
user_config_file = user_config_dir + "/gq.ini"
config = configparser.ConfigParser()


def add_section_if_not_exists(config, section_name):
    if not config.has_section(section_name):
        config.add_section(section_name)


