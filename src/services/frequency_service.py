"""services.frequency_service"""
#########################################################
# Builtin packages
#########################################################
from collections import Counter
from dataclasses import dataclass

#########################################################
# 3rd party packages
#########################################################
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

#########################################################
# Own packages
#########################################################
from common.config import FREQUENCY_PATH, TARGET_PATH
from common.decorator import exception_module
from common.log import info
from models import Vocabulary
from models import Frequency
from models import PartOfSpeech
from repositories.frequencies import CsvFrequencyRepository
from repositories.frequencies import GssFrequencyRepository
from utils import has_file, make_file


@dataclass
class FrequencyService(object):
    """frequency service"""

    def __init__(self):
        self.csv_repo = CsvFrequencyRepository()
        self.gss_repo = GssFrequencyRepository()

    def __create_csv_path(self, additional_filename):
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        path = f"{FREQUENCY_PATH}/frequency_{additional_filename}_{file_name}{extension}"
        return path

    @exception_module
    def add(self, freqs: list[Frequency,], csv_filename: str | None = None, gss_sheet_name: str | None = None):
        if csv_filename:
            self.csv_repo.path = self.__create_csv_path(csv_filename)
        if gss_sheet_name:
            self.gss_repo.sheet_name = gss_sheet_name
            self.gss_repo.update_sheet_name(gss_sheet_name)

        self.write_csv(freqs)
        self.write_gss(freqs)

    @ exception_module
    def write_csv(self, freqs: list[Frequency, ], output_path: str | None = None) -> None:
        if output_path:
            path = self.csv_repo.path
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(freqs, path=output_path)

    @ exception_module
    def write_gss(self, freqs: list[Frequency, ]) -> None:
        self.gss_repo.add(freqs)

    @ exception_module
    def add_by_pos(self, pos: PartOfSpeech) -> None:
        attrs = pos.attributes
        for attr in attrs:
            vocabs = pos.get_values(attr)
            output_path = f"/pos/{attr}"
            freqs = self.calculate_vocab_frequencies(vocabs)
            self.write_csv(freqs, output_path=output_path)

    @ exception_module
    def calculate_vocab_frequencies(self, vocabs: list[Vocabulary,]) -> list[Frequency, ]:
        info("calculate vocabulary frequencies")
        vocabs_original_form = [vocab.original_form for vocab in vocabs]
        vocab_freqs = dict(Counter(vocabs_original_form).most_common())

        freqs = []
        id_ = 1
        for vocab, times in vocab_freqs.items():
            vocab_obj = next(v for v in vocabs if v.original_form == vocab)
            freq = Frequency(id=id_,
                             vocabulary=vocab,
                             level=vocab_obj.level,
                             eiken_level=vocab_obj.eiken_level,
                             school_level=vocab_obj.school_level,
                             toeic_level=vocab_obj.toeic_level,
                             times=times)
            freqs.append(freq)
            id_ += 1
        info("calculated vocabulary frequencies: {0}", len(freqs))
        return freqs
