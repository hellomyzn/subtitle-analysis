"""utils.helper"""
#########################################################
# Builtin packages
#########################################################
import os

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common import log


def ls(path: str) -> list:
    """return file names like ls.

    Args:
        path (str): dir path

    Returns:
        list: file names
    """
    try:
        files = os.listdir(path)
    except FileNotFoundError as exc:
        log.warn(exc)
        files = []

    return files


def get_file_path(dir_path):
    file_names = ls(dir_path)
    file_name = file_names[0]
    if not file_names:
        log.warn("failed to get subtitles since the file path was not found. path: {0}",
                 dir_path)
    path = f"{dir_path}/{file_name}"
    return path
