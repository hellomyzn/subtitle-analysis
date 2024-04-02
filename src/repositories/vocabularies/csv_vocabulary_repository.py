"""repositories.vocabularies.csv_vocabulary_repository"""
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
from common.config import VOCABULARY_PATH, TARGET_PATH
from models import Vocabulary
from repositories import CsvBaseRepository
from repositories import ModelAdapter
from utils import has_file, make_file


class CsvVocabularyRepository(CsvBaseRepository):
    """csv sentence repository"""

    KEY_ID = "id"
    KEY_VOCABULARY = "vocabulary"
    KEY_POS = "pos"
    KEY_SENTENCE_ID = "sentence_id"
    HEADER = [KEY_ID, KEY_VOCABULARY, KEY_POS, KEY_SENTENCE_ID]
    adapter: ModelAdapter = ModelAdapter(Vocabulary, {
        "id": KEY_ID,
        "vocabulary": KEY_VOCABULARY,
        "pos": KEY_POS,
        "sentence_id": KEY_SENTENCE_ID})

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{VOCABULARY_PATH}/vocabulary_{file_name}{extension}"
        if not has_file(path):
            make_file(path)
        super().__init__(path, self.HEADER, self.adapter)
