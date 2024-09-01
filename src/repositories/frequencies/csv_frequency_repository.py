"""repositories.frequencies.csv_frequency_repository"""
#########################################################
# Builtin packages
#########################################################
import csv

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.config import FREQUENCY_PATH, TARGET_PATH
from models import Frequency
from repositories import CsvBaseRepository
from repositories import ModelAdapter
from utils import has_file, make_file


class CsvFrequencyRepository(CsvBaseRepository):
    """csv frequency repository"""

    KEY_ID = "id"
    KEY_VOCABULARY = "vocabulary"
    KEY_TIME = "times"
    KEY_LEVEL = "level"
    KEY_EIKEN_LEVEL = "eiken_level"
    KEY_SCHOOL_LEVEL = "school_level"
    KEY_TOEIC_LEVEL = "toeic_level"
    HEADER = [KEY_ID, KEY_VOCABULARY, KEY_TIME, KEY_LEVEL,
              KEY_EIKEN_LEVEL, KEY_SCHOOL_LEVEL, KEY_TOEIC_LEVEL]
    adapter: ModelAdapter = ModelAdapter(Frequency, {
        "id": KEY_ID,
        "vocabulary": KEY_VOCABULARY,
        "times": KEY_TIME,
        "level": KEY_LEVEL,
        "eiken_level": KEY_EIKEN_LEVEL,
        "school_level": KEY_SCHOOL_LEVEL,
        "toeic_level": KEY_TOEIC_LEVEL})

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{FREQUENCY_PATH}/frequency_{file_name}{extension}"

        if not has_file(path):
            make_file(path)

        super().__init__(path, self.HEADER, self.adapter)

    def get_by_pos(self, pos: str) -> list[Frequency, ]:
        path = self.path
        dir_path = "/".join(path.split("/")[:-1]) + "/pos"
        filename = f"{pos}_{path.split('/')[-1]}"
        input_path = f"{dir_path}/{filename}"

        with open(input_path, encoding="utf-8", mode="r") as f:
            reader = csv.DictReader(f)
            freqs = [Frequency.from_dict(row) for row in reader]

        return freqs
