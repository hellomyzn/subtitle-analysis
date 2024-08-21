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
    KEY_ENGLISH = "english"
    KEY_MEANING = "meaning"
    KEY_POS = "pos"
    KEY_ORIGINAL_FORM = "original"
    KEY_LEVEL = "level"
    KEY_EIKEN_LEVEL = "eiken_level"
    KEY_SCHOOL_LEVEL = "school_level"
    KEY_TOEIC_LEVEL = "toeic_level"
    KEY_SUBJECT_ID = "subject_id"
    HEADER = [KEY_ID, KEY_ENGLISH, KEY_MEANING, KEY_POS, KEY_ORIGINAL_FORM, KEY_LEVEL,
              KEY_EIKEN_LEVEL, KEY_SCHOOL_LEVEL, KEY_TOEIC_LEVEL, KEY_SUBJECT_ID]
    adapter: ModelAdapter = ModelAdapter(Vocabulary, {
        "id": KEY_ID,
        "english": KEY_ENGLISH,
        "meaning": KEY_MEANING,
        "pos": KEY_POS,
        "original": KEY_ORIGINAL_FORM,
        "level": KEY_LEVEL,
        "eiken_level": KEY_EIKEN_LEVEL,
        "school_level": KEY_SCHOOL_LEVEL,
        "toeic_level": KEY_TOEIC_LEVEL,
        "subject_id": KEY_SUBJECT_ID})

    def __init__(self):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{VOCABULARY_PATH}/vocabulary_{file_name}{extension}"
        if not has_file(path):
            make_file(path)
        super().__init__(path, self.HEADER, self.adapter)
