"""repositories.sentences.csv_sentence_repository"""
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
from common.config import SUBS_CSV_PATH, TARGET_PATH
from models import Subtitle
from repositories import CsvBaseRepository
from repositories import ModelAdapter
from utils import has_file, make_file


class CsvSubtitleRepository(CsvBaseRepository):
    """csv sentence repository"""

    KEY_ID = "id"
    KEY_SENTENCE = "sentence"
    HEADER = [KEY_ID, KEY_SENTENCE]
    adapter: ModelAdapter = ModelAdapter(Subtitle, {
        "id": KEY_ID,
        "sentence": KEY_SENTENCE})

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{SUBS_CSV_PATH}/subtitle_{file_name}{extension}"

        if not has_file(path):
            make_file(path)

        super().__init__(path, self.HEADER, self.adapter)
