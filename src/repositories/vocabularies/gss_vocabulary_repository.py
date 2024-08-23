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

    KEY_ID = "id"
    KEY_WORD = "word"
    KEY_MEANING = "meaning"
    KEY_POS = "pos"
    KEY_ORIGINAL_FORM = "original_form"
    KEY_LEVEL = "level"
    KEY_EIKEN_LEVEL = "eiken_level"
    KEY_SCHOOL_LEVEL = "school_level"
    KEY_TOEIC_LEVEL = "toeic_level"
    KEY_SUBTITLE_ID = "subtitle_id"
    COLUMNS = [KEY_ID, KEY_WORD, KEY_MEANING, KEY_POS, KEY_ORIGINAL_FORM, KEY_LEVEL,
               KEY_EIKEN_LEVEL, KEY_SCHOOL_LEVEL, KEY_TOEIC_LEVEL, KEY_SUBTITLE_ID]

    def __init__(self, sheet_name: str = "vocabulary"):
        adapter: ModelAdapter = ModelAdapter(Vocabulary, {
            "id": self.KEY_ID,
            "word": self.KEY_WORD,
            "meaning": self.KEY_MEANING,
            "pos": self.KEY_POS,
            "original_form": self.KEY_ORIGINAL_FORM,
            "level": self.KEY_LEVEL,
            "eiken_level": self.KEY_EIKEN_LEVEL,
            "school_level": self.KEY_SCHOOL_LEVEL,
            "toeic_level": self.KEY_TOEIC_LEVEL,
            "subtitle_id": self.KEY_SUBTITLE_ID})
        super().__init__(sheet_name, self.COLUMNS, adapter)
