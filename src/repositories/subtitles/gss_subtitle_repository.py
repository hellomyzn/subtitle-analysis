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
    COLUMNS = [KEY_ID, KEY_SENTENCE]

    def __init__(self):
        adapter: ModelAdapter = ModelAdapter(Subtitle, {
            "id": self.KEY_ID,
            "sentence": self.KEY_SENTENCE})
        super().__init__(self.SHEET_NAME, self.COLUMNS, adapter)
