"""utils.helper"""
#########################################################
# Builtin packages
#########################################################
import os
import pathlib
from typing import Any

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


def has_file(path: str) -> bool:
    return os.path.isfile(path)


def make_file(path: str) -> None:
    try:
        path, extension = path.split(".")
        dir_path = "/".join(path.split("/")[:-1])
    except ValueError:
        extension = None

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    if extension:
        pathlib.Path(f"{path}.{extension}").touch()


def get_index_number(list_: list[Any], val) -> int | None:
    """
    Get the index of a value in a list.

    Args:
        list_ (list): The list to search.
        val: The value to find.

    Returns:
        int | None: The index of the value if found; otherwise, None.
    """
    try:
        return list_.index(val)
    except ValueError:
        return None


def get_value_by_idx(list_: list[Any], idx: int) -> Any | None:
    """
    Get a value from a list by its index.

    Args:
        list_ (list[Vocabulary]): The list to retrieve the value from.
        idx (int): The index of the value.

    Returns:
        any | None: The value at the specified index if it exists; otherwise, None.
    """
    if 0 <= idx < len(list_):
        return list_[idx]
    return None
