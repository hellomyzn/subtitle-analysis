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
    KEY_POS = "pos"
    KEY_SUBJECT_ID = "subject_id"
    COLUMNS = [KEY_ID, KEY_ENGLISH, KEY_POS, KEY_SUBJECT_ID]

    def __init__(self):
        adapter: ModelAdapter = ModelAdapter(Vocabulary, {
            "id": self.KEY_ID,
            "english": self.KEY_ENGLISH,
            "pos": self.KEY_POS,
            "subject_id": self.KEY_SUBJECT_ID})
        super().__init__(self.SHEET_NAME, self.COLUMNS, adapter)
