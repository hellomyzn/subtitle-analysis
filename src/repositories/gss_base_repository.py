"""repositories.gss_base_repository"""
#########################################################
# Builtin packages
#########################################################
import time
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
import gspread

#########################################################
# Own packages
#########################################################
from common.config import Config
from common.google_spreadsheet import GssAccessor
from common.log import (
    error,
    warn,
    info
)
from repositories import BaseRepositoryInterface
from requests.exceptions import ConnectionError


CONFIG = Config().config
SHEET_KEY = CONFIG["GSS"]["SHEET_KEY"]


@dataclass
class GssBaseRepository(BaseRepositoryInterface):
    """gss base repository"""

    SHEET_SIZE_ERR_STATUS = "INVALID_ARGUMENT"
    REQUEST_LIMIT_ERR_STATUS = "RESOURCE_EXHAUSTED"
    ROW_NUM_TO_ADD = 1000

    sheet_name: gspread = field(init=False, default=None)
    columns: list = field(init=False, default_factory=list)

    def __init__(self, sheet_name, columns):
        self.sheet_name = sheet_name
        self.columns = columns
        gss = GssAccessor()
        workbook = gss.connection.open_by_key(SHEET_KEY)
        self.worksheet = workbook.worksheet(sheet_name)

        if not self.__has_columns():
            self.__write_columns()

    def all(self) -> list:
        pass

    def find_by_id(self, id_: int) -> dict:
        pass

    def add(self, data: dict) -> None:
        """_summary_

        Args:
            data (dict): _description_

        Raises:
            gspread.exceptions.APIError: _description_
            ConnectionError: _description_
        """
        values = list(data.values())
        attempts = 1
        max_attempts = 3

        while attempts <= max_attempts:
            try:
                row_num = self.__find_next_available_row()
                self.worksheet.insert_row(values, row_num)
            except ConnectionError as err:
                attempts += 1
                is_connection_err = True
                warn("connection error. {0}: {1}", err.__class__.__name__, err)
                time.sleep(30)
            except gspread.exceptions.APIError as err:
                err_status = err.response.json()["error"]["status"]
                is_sheet_size_err = bool(err_status == self.SHEET_SIZE_ERR_STATUS)
                is_request_limit = bool(err_status == self.REQUEST_LIMIT_ERR_STATUS)

                if is_sheet_size_err:
                    # no row to add new data in the sheet.
                    warn("sheet size(row) is not enough. {0}: {1}", err.__class__.__name__, err)
                    time.sleep(10)
                    self.worksheet.add_rows(self.ROW_NUM_TO_ADD)
                    info("added {0} rows in the sheet({1})", self.ROW_NUM_TO_ADD, self.sheet_name)
                elif is_request_limit:
                    # request quota exceeded the limit
                    warn("request quota exceeded the limit. {0}: {1}", err.__class__.__name__, err)
                    time.sleep(60)
                else:
                    attempts += 1
                    mes = ("failed to add data into gss 3 times. ",
                           "please check the log. "
                           f"{err.__class__.__name__}: {err}")
                    error(mes)
                    raise gspread.exceptions.APIError(mes)
            else:
                # success
                info("added data in the gss({0}).", self.sheet_name)
                is_connection_err = False
                break

        if is_connection_err:
            mes = ("failed to connect to gss 3 times. ",
                   "please check your internet connection.")
            error(mes)
            raise ConnectionError(mes)

        time.sleep(1)

    def delete_by_id(self, id_: int) -> None:
        pass

    def __has_columns(self) -> bool:
        """check the sheet has columns or not

        Returns:
            bool: the sheet has columns or not
        """
        columns = self.worksheet.row_values(1)
        time.sleep(1)
        return bool(columns == self.columns)

    def __write_columns(self) -> None:
        """write columns on the sheet
        """
        self.worksheet.insert_row(self.columns, index=1)
        info("added columns in the gss({0}). value: {1}",
             self.sheet_name, self.columns)
        time.sleep(1)

    def __find_next_available_row(self) -> int:
        """ Find a next available row on GSS
            This is for confirming from which row is available
            when you add data on GSS.

        Returns:
            int: _description_
        """
        # it is a list which contains all data on first column
        fist_column_data = list(filter(None, self.worksheet.col_values(1)))
        time.sleep(1)
        available_row = int(len(fist_column_data)) + 1
        return available_row
