"""services.subtitle_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass

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
from repositories.subtitles import GssSubtitleRepository


@dataclass
class SubtitleService(object):
    """subtitle service"""

    def __init__(self):
        self.srt_repo = SrtSubtitleRepository()
        self.csv_repo = CsvSubtitleRepository()
        self.gss_repo = GssSubtitleRepository()

    @exception_module
    def add(self, subs: list[Subtitle, ]) -> None:
        self.write_csv(subs)
        self.write_gss(subs)

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

    @exception_module
    def write_gss(self, subs: list[Subtitle, ]) -> None:
        """write subtitle on gss

        Args:
            subs (list[Subtitle, ]): subtitles
        """
        self.gss_repo.add(subs)
