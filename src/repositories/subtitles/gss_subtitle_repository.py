"""repositories.subtitles.gss_subtitle_repository"""
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
from models import Subtitle
from repositories import GssBaseRepository
from repositories import ModelAdapter


class GssSubtitleRepository(GssBaseRepository):
    """gss subtitle repository"""

    SHEET_NAME = "subtitle"

    KEY_ID = "id"
    KEY_SENTENCE = "sentence"
    KEY_TIME_FROM = "time_from"
    KEY_TIME_TO = "time_to"
    COLUMNS = [KEY_ID, KEY_SENTENCE, KEY_TIME_FROM, KEY_TIME_TO]

    def __init__(self):
        adapter: ModelAdapter = ModelAdapter(Subtitle, {
            "id": self.KEY_ID,
            "sentence": self.KEY_SENTENCE,
            "time_from": self.KEY_TIME_FROM,
            "time_to": self.KEY_TIME_TO, })
        super().__init__(self.SHEET_NAME, self.COLUMNS, adapter)
