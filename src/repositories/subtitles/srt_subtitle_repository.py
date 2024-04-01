
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
from common.config import Config
from common.log import info
from utils import get_file_path

config = Config().config


@dataclass
class SrtSubtitleRepository(object):
    """srt subtitle repository"""
    path: str = field(init=False, default=None)

    def __init__(self):
        target_path = config["SUBS"]["PATH"]
        dir_path = f"/opt/work/src/subtitles/{target_path}"
        path = get_file_path(dir_path)
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
        sentences = self.__format(lines)
        info("get subtitles successfully. lines: {0}", len(sentences))
        return sentences

    def __format(self, lines: list) -> list:
        """format subtitles

        Args:
            lines (list): subtitles

        Returns:
            list: formatted sentence form subtitles
        """
        sentences = []
        id_ = 1
        for line in lines:
            if self.__is_not_subtitle(line):
                continue
            line = self.__remove_symbols(line)

            first_letter = line[0]
            if first_letter.islower():
                previous_line = sentences[-1]
                previous_line["sentence"] += f" {line}"
                continue

            sentence = {"id": id_, "sentence": str(line)}
            sentences.append(sentence)
            id_ += 1
        return sentences

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
