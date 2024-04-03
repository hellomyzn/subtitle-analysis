"""services.subtitle_service"""
#########################################################
# Builtin packages
#########################################################
import csv
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.decorator import exception_module
from models import Subtitle
from repositories.subtitles import SrtSubtitleRepository
from repositories.subtitles import CsvSubtitleRepository
from repositories.vocabularies import CsvVocabularyRepository
from repositories.frequencies import CsvFrequencyRepository


@dataclass
class SubtitleService(object):
    """subtitle service"""

    def __init__(self):
        self.srt_repo = SrtSubtitleRepository()
        self.csv_repo = CsvSubtitleRepository()

    @exception_module
    def get_from_srt(self) -> list[Subtitle, ]:
        """get subtitles from srt file

        Returns:
            list[Subtitle, ]: subtitles
        """
        subs = self.srt_repo.get()
        return subs

    @exception_module
    def write_csv(self, subs: list[Subtitle, ]) -> None:
        """write subtitle on csv

        Args:
            subs (list[Subtitle, ]): subtitles
        """
        self.csv_repo.write(subs)
