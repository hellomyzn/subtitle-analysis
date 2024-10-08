"""common.decorator.decorator for exception"""
#########################################################
# Builtin packages
#########################################################
import json
import functools
import time
import traceback
import sys
import requests

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import error, warn, info
from common.exceptions import (
    MyException,
    MyRequestsException,
    MyJsonDecodeException,
    MyGssException,
    MyGssInvalidArgumentException,
    MyGssResourceExhaustedException
)


def __get_request_info(exc: requests.exceptions.RequestException) -> dict | str:
    """Request exception info

    Args:
        exc (requests.exceptions.RequestException): requests exception

    Returns:
        dict | str: requests info
    """
    if isinstance(exc.request, requests.models.PreparedRequest):
        request_info = {
            "method": exc.request.method,
            "url": exc.request.url,
            "headers": exc.request.headers,
            "body": exc.request.body
        }
    else:
        request_info = "Exception does not contain Request"

    return request_info


def __get_response_info(exc: requests.exceptions.RequestException) -> dict | str:
    """Response exception info

    Args:
        exc (requests.exceptions.RequestException): response exception

    Returns:
        dict | str: response info
    """
    if isinstance(exc.response, requests.models.Response):
        response_info = {
            "status_code": exc.response.status_code,
            "body": exc.response.text
        }
    else:
        response_info = "Exception does not contain Response"

    return response_info


def exception_module(func):
    """_summary_

    Args:
        func (_type_): _description_
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as exc:
            request_info = __get_request_info(exc)
            response_info = __get_response_info(exc)
            mes = (f"RequestException occurred. exc: {str(exc)} "
                   f"request_info: {request_info}, response_info: {response_info}")
            error(mes)
            raise MyRequestsException(mes) from exc
        except json.JSONDecodeError as exc:
            mes = f"JSON Decode Error occurred. input: {exc.doc}, exc: {exc}"
            error(mes)
            raise MyJsonDecodeException(mes) from exc
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            t_str = " ".join(traceback.format_exception(exc_type, exc_obj, exc_tb))
            mes = f"SystemException occurred. traceback: {t_str}"
            error(mes)
            raise MyException(mes) from exc

    return wrapper


def gss_module(func):
    """_summary_

    Args:
        func (_type_): _description_

    Raises:
        MyGssException: _description_

    Returns:
        _type_: _description_
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 1
        max_attempts = 3
        while attempts <= max_attempts:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError as exc:
                sec = 30
                warn("connection error. {0}: {1}", exc.__class__.__name__, exc)
            except MyGssInvalidArgumentException:
                sec = 5
            except MyGssResourceExhaustedException:
                sec = 60
            except MyGssException:
                sec = 1
            attempts += 1
            warn("wait {0} sec", sec)
            time.sleep(sec)

        # failed
        mes = ("failed to connect to gss 3 times. "
               "please check your internet connection or logs.")
        error(mes)
        raise MyGssException(mes)
    return wrapper
