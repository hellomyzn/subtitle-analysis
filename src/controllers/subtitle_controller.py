"""controllers.subtitle_controller"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from services import SubtitleService


@dataclass
class SubtitleController(object):
    """subtitle controller"""
    service: SubtitleService = field(default=None, init=False)

    def __init__(self):
        self.service = SubtitleService()

    def add(self):
        """analyze vocabularies from subtitles and add to repository
        """
        self.service.add()
