"""repositories.frequencies.csv_frequency_repository"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.config import FREQUENCY_PATH, TARGET_PATH
from models import Sentence
from repositories import CsvBaseRepository
from repositories import ModelAdapter
from utils import has_file, make_file


class CsvFrequencyRepository(CsvBaseRepository):
    """csv frequency repository"""

    KEY_ID = "id"
    KEY_VOCABULARY = "vocabulary"
    KEY_FREQUENCY = "frequency"
    HEADER = [KEY_ID, KEY_VOCABULARY, KEY_FREQUENCY]
    adapter: ModelAdapter = ModelAdapter(Sentence, {
        "id": KEY_ID,
        "vocabulary": KEY_VOCABULARY,
        "frequency": KEY_FREQUENCY})

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{FREQUENCY_PATH}/pos/frequency_{file_name}{extension}"

        if not has_file(path):
            make_file(path)

        super().__init__(path, self.HEADER, self.adapter)
