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
    COLUMNS = [KEY_ID, KEY_VOCABULARY, KEY_TIME]

    def __init__(self, sheet_name="frequency"):
        self.sheet_name = sheet_name
        adapter: ModelAdapter = ModelAdapter(Frequency, {
            "id": self.KEY_ID,
            "vocabulary": self.KEY_VOCABULARY,
            "times": self.KEY_TIME})
        super().__init__(self.sheet_name, self.COLUMNS, adapter)
