"""repositories.gss_base_repository"""
#########################################################
# Builtin packages
#########################################################
import time
from dataclasses import dataclass

#########################################################
# 3rd party packages
#########################################################
import gspread

#########################################################
# Own packages
#########################################################
from common.config import Config
from common.decorator import gss_module
from common.exceptions import (MyGssException,
                               MyGssInvalidArgumentException,
                               MyGssResourceExhaustedException)
from common.google_spreadsheet import GssAccessor
from common.log import warn, info, debug
from models import Model
from repositories import BaseRepositoryInterface


CONFIG = Config().config
SHEET_KEY = CONFIG["GSS"]["SHEET_KEY"]


@dataclass
class GssBaseRepository(BaseRepositoryInterface):
    """gss base repository"""

    def __init__(self, sheet_name, columns, adapter):
        self.sheet_name = sheet_name
        self.columns = columns
        self.adapter = adapter
        gss = GssAccessor()
        workbook = gss.connection.open_by_key(SHEET_KEY)
        self.worksheet = workbook.worksheet(sheet_name)

        if not self.__has_columns():
            self.__write_columns()

    def all(self) -> list:
        pass

    def find_by_id(self, id_: int) -> dict:
        pass

    @gss_module
    def add(self, data: list[Model, ]) -> None:
        """_summary_

        Args:
            data (list[Model, ]): _description_

        Raises:
            MyGssInvalidArgumentException: _description_
            MyGssResourceExhaustedException: _description_
            MyGssException: _description_
        """
        inputs = []

        for model in data:
            input_ = self.adapter.from_model_to_list(model)
            inputs.append(input_)

        row_num = self.__find_next_available_row()
        try:
            debug("data: {0}, row_num: {1}", len(inputs), row_num)
            self.worksheet.insert_rows(inputs, row_num)
        except gspread.exceptions.APIError as exc:
            err_status = exc.response.json()["error"]["status"]
            is_sheet_size_err = bool(err_status == "INVALID_ARGUMENT")
            is_request_limit = bool(err_status == "RESOURCE_EXHAUSTED")
            if is_sheet_size_err:
                # no row to add new data in the sheet.
                warn("sheet size(row) is not enough. {0}: {1}",
                     exc.__class__.__name__, exc)
                rows_to_add = 1000
                self.worksheet.add_rows(rows_to_add)
                info("added {0} rows in the sheet({1})", rows_to_add, self.sheet_name)
                raise MyGssInvalidArgumentException(exc) from exc
            if is_request_limit:
                # request quota exceeded the limit
                warn("gspread api error: request quota exceeded the limit. {0}: {1}",
                     exc.__class__.__name__, exc)
                raise MyGssResourceExhaustedException(exc) from exc
            warn("gspread api error: please check log out. {0}: {1}",
                 exc.__class__.__name__, exc)
            raise MyGssException(exc) from exc

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
