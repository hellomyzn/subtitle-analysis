
"""repositories.subtitles.srt_subtitle_repository"""
#########################################################
# Builtin packages
#########################################################
import re
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.config import SUBS_PATH
from common.log import info, warn
from models import Subtitle
from utils import get_file_path


@dataclass
class SrtSubtitleRepository(object):
    """srt subtitle repository"""
    path: str = field(init=False, default=None)

    def __init__(self):
        path = get_file_path(SUBS_PATH)
        self.path = path

    def get(self) -> list[dict[int, str],]:
        """get subtitles

        Returns:
            list[dict[int, str],]: sentences
        """
        # read
        with open(file=self.path, mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        # format
        sentences = self.__parse_to_sentence(lines)
        info("get subtitles successfully. lines: {0}", len(sentences))
        return sentences

    def gets(self) -> list[dict[int, str],]:
        """get subtitles

        Returns:
            list[dict[int, str],]: sentences
        """
        from utils.helper import ls
        lines_list = []

        for dir in ls(SUBS_PATH):
            if "." in dir:
                continue
            if "all" in dir:
                continue

            subs_ep_path = f"{SUBS_PATH}/{dir}"
            self.path = get_file_path(subs_ep_path)

            # read
            with open(file=self.path, mode="r", encoding="utf-8") as file:
                lines_list += file.readlines()

        # format
        sentences = self.__parse_to_sentence(lines_list)
        info("get subtitles successfully. lines: {0}", len(sentences))
        return sentences

    def __parse_to_sentence(self, lines: list) -> list:
        """format subtitles

        Args:
            lines (list): subtitles

        Returns:
            list: formatted sentence form subtitles
        """
        sentences = []
        id_ = 1
        time_from = None
        time_to = None
        for line in lines:
            if self.__is_time_range(line):
                time_from, time_to = self.__retrieve_time_range(line)
            if self.__is_not_subtitle(line):
                continue
            line = self.__remove_symbols(line)

            first_letter = line[0]
            if first_letter.islower():
                previous_line = sentences[-1]
                previous_line.sentence += f" {line}"
                continue

            sentence = Subtitle(id=id_, sentence=str(line), time_from=time_from, time_to=time_to)
            sentences.append(sentence)
            id_ += 1
        return sentences

    @staticmethod
    def __is_time_range(line: str) -> bool:
        """check it is time range or not
            e.g. 00:00:52,969 --> 00:00:55,137

        Args:
            line (str): subtitle

        Returns:
            bool: if it is time range, True. but False
        """
        time_pattern = r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})'
        return re.match(time_pattern, line)

    @staticmethod
    def __retrieve_time_range(line: str) -> tuple[str | None, str | None]:
        """ retrieve time range as from and to
            e.g. 00:00:52,969 --> 00:00:55,137

        Args:
            line (str): subtitle

        Returns:
            tuple[str | None, str | None]: time range but if it is not, None
        """
        time_from = None
        time_to = None
        time_pattern = r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})'
        match = re.match(time_pattern, line)
        if match:
            time_from = match.group(1)
            time_to = match.group(2)
        return time_from, time_to

    @staticmethod
    def __is_not_subtitle(line: str) -> bool:
        """check line is subtitle or not

            subtile file includes some unnecessary texts for subtitle
            so remove the texts using re
            e.g.
                1
                00:00:47,881 --> 00:00:49,757
                [CAR HORNS HONKING]

                2
                00:00:49,966 --> 00:00:52,760
                There's nothing to tell.
                It's just some guy I work with.
            True:
                There's nothing to tell.
                It's just some guy I work with.
            False
                1
                00:00:47,881 --> 00:00:49,757
                [CAR HORNS HONKING]

                2
                00:00:49,966 --> 00:00:52,760

        Args:
            line (str): texts

        Returns:
            bool: True: subtitle, False: not subtitle
        """
        time_pattern = r'\b\d{2}:\d{2}:\d{2}\b'
        square_brackets_pattern = r'\[(.*?)\]'
        number_pattern = r'\b\d+\b'
        newline_pattern = r'\n'

        patterns = [time_pattern,
                    square_brackets_pattern,
                    number_pattern,
                    newline_pattern]

        return any(re.match(pattern, line) for pattern in patterns)

    @staticmethod
    def __remove_symbols(line: str) -> str:
        """remove noises/symbols from subtitle

        Args:
            line (str): texts

        Returns:
            str: sentence removed noises/symbols
        """
        symbols_right = ["\"", "\'", "\n",  "!", "?", ".", ","]
        symbols_left = ["\"", "\'", "- ", "\n", "..."]
        for symbol in symbols_right:
            line = line.rstrip(symbol)
        for symbol in symbols_left:
            line = line.lstrip(symbol)
        return line
