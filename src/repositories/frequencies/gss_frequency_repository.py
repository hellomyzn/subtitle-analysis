"""repositories.frequencies.gss_frequency_repository"""
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
from models import Frequency
from repositories import GssBaseRepository
from repositories import ModelAdapter


class GssFrequencyRepository(GssBaseRepository):
    """gss frequency repository"""

    KEY_ID = "id"
    KEY_VOCABULARY = "vocabulary"
    KEY_TIME = "times"
    KEY_LEVEL = "level"
    KEY_EIKEN_LEVEL = "eiken_level"
    KEY_SCHOOL_LEVEL = "school_level"
    KEY_TOEIC_LEVEL = "toeic_level"
    COLUMNS = [KEY_ID, KEY_VOCABULARY, KEY_TIME, KEY_LEVEL,
               KEY_EIKEN_LEVEL, KEY_SCHOOL_LEVEL, KEY_TOEIC_LEVEL]

    def __init__(self, sheet_name="frequency"):
        self.sheet_name = sheet_name
        adapter: ModelAdapter = ModelAdapter(Frequency, {
            "id": self.KEY_ID,
            "vocabulary": self.KEY_VOCABULARY,
            "times": self.KEY_TIME,
            "level": self.KEY_LEVEL,
            "eiken_level": self.KEY_EIKEN_LEVEL,
            "school_level": self.KEY_SCHOOL_LEVEL,
            "toeic_level": self.KEY_TOEIC_LEVEL})
        super().__init__(self.sheet_name, self.COLUMNS, adapter)
