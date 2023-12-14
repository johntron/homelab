from bootserver import distro_files, config_yaml


def prepare():
    distro_files.netboot_files()
    config_yaml.write_configs()
