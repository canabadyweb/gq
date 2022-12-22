def add_section_if_not_exists(config, section_name):
    if not config.has_section(section_name):
        config.add_section(section_name)


