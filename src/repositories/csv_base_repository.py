"""repositories.csv_base_repository"""
#########################################################
# Builtin packages
#########################################################
import csv
import sys
from dataclasses import dataclass, field


#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import (
    error,
    warn,
    info
)
from repositories import BaseRepositoryInterface


@dataclass
class CsvBaseRepository(BaseRepositoryInterface):
    """csv base repository"""

    path: str = field(init=True, default=None)
    header: list = field(init=True, default_factory=list)

    def all(self) -> list:
        """get all data from csv

        Returns:
            list: all data from csv
        """
        if not self.__has_header():
            self.__write_header()

        with open(self.path, encoding="utf-8", mode="r") as f:
            reader = csv.DictReader(f)
            all_data = [row for row in reader]
        return all_data

    def find_by_id(self, id_: int) -> dict:
        pass

    def add(self, data: dict) -> None:
        """add data into the csv file

        Args:
            data (dict): data to add
        """
        if not self.__has_header():
            self.__write_header()

        with open(self.path, encoding="utf-8", mode="a") as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writerow(data)

        info("added data in the csv file({0}).", self.path)

    def delete_by_id(self, id_: int) -> None:
        pass

    def __has_header(self) -> bool:
        """check the csv file has header or not

        Returns:
            bool: the csv file has header or not
        """
        with open(self.path, encoding="utf-8", mode="r") as f:
            reader = csv.DictReader(f)

            header = reader.fieldnames
            if header is None:
                warn("header is None in the csv file({0}).", self.path)
            elif header != self.header:
                error("invalid header in the csv file({0}): {1}, expected header: {2}",
                      self.path, header, self.header)
                sys.exit(1)

        return bool(header)

    def __write_header(self) -> None:
        """write header
        """
        with open(self.path, encoding="utf-8", mode="w") as file:
            writer_ = csv.DictWriter(file, fieldnames=self.header)
            writer_.writeheader()
            info(f"write header in the csv file({0}). header: {1}",
                 self.path, self.header)
