#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :  config.py
@Time    :  2023/03/24 10:13:47
@Author  :  zoro.chang
"""

from pathlib import Path
from enum import Enum
import yaml

project_folder_path = Path(__file__).resolve().parent.parent
config_path = project_folder_path.joinpath('configs', 'config.yaml')
if config_path.is_file():
    with open(config_path, 'r', encoding="utf-8") as file:
        data_loaded = yaml.safe_load(file)
else:
    raise FileNotFoundError(f"No config.yaml found, please check that the file has been placed at {config_path}")

def path_decider(path):
    path = Path(path).resolve()
    if path.is_absolute():
        return path
    return project_folder_path.joinpath(path)

class ProjectConfigs(Enum):
    USER_INFO_PATH = Path(path_decider(data_loaded["DATA"]["USER_INFO_PATH"]))
