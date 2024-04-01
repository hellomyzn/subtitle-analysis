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
from common.config import SENTENCE_PATH, TARGET_PATH
from repositories import CsvBaseRepository
from utils import has_file, make_file


class CsvSentenceRepository(CsvBaseRepository):
    """csv sentence repository"""

    KEY_ID = "id"
    KEY_SENTENCE = "sentence"
    HEADER = [KEY_ID, KEY_SENTENCE]

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{SENTENCE_PATH}/sentence_{file_name}{extension}"

        if not has_file(path):
            make_file(path)

        super().__init__(path, self.HEADER)
