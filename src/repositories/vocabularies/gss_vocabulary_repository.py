"""repositories.vocabularies.gss_vocabulary_repository"""
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
from models import Vocabulary
from repositories import GssBaseRepository
from repositories import ModelAdapter


class GssVocabularyRepository(GssBaseRepository):
    """gss vocabulary repository"""

    SHEET_NAME = "vocabulary"

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
    COLUMNS = [KEY_ID, KEY_ENGLISH, KEY_MEANING, KEY_POS, KEY_ORIGINAL_FORM, KEY_LEVEL,
               KEY_EIKEN_LEVEL, KEY_SCHOOL_LEVEL, KEY_TOEIC_LEVEL, KEY_SUBJECT_ID]

    def __init__(self):
        adapter: ModelAdapter = ModelAdapter(Vocabulary, {
            "id": self.KEY_ID,
            "english": self.KEY_ENGLISH,
            "meaning": self.KEY_MEANING,
            "pos": self.KEY_POS,
            "original": self.KEY_ORIGINAL_FORM,
            "level": self.KEY_LEVEL,
            "eiken_level": self.KEY_EIKEN_LEVEL,
            "school_level": self.KEY_SCHOOL_LEVEL,
            "toeic_level": self.KEY_TOEIC_LEVEL,
            "subject_id": self.KEY_SUBJECT_ID})
        super().__init__(self.SHEET_NAME, self.COLUMNS, adapter)
