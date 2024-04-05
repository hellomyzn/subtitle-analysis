"""services.vocabulary_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass

#########################################################
# 3rd party packages
#########################################################
import nltk

#########################################################
# Own packages
#########################################################
from common.decorator import exception_module
from models import Subtitle
from models import Vocabulary
from repositories.vocabularies import CsvVocabularyRepository
from repositories.vocabularies import GssVocabularyRepository
from utils import has_file, make_file


@dataclass
class VocabularyService(object):
    """vocabulary service"""

    def __init__(self):
        self.csv_repo = CsvVocabularyRepository()
        self.gss_repo = GssVocabularyRepository()

    @exception_module
    def add(self, vocabs: list[Vocabulary, ]):
        self.write_csv(vocabs)
        self.write_gss(vocabs)

    @exception_module
    def extract_from_subtitles(self, subs: list[Subtitle, ]):
        """extract vocabulary from sentence using nltk package

        Args:
            subs (list): english subtitles

        Returns:
            list[Vocabulary,]: vocabularies splitted by nltk
        """
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        vocabularies = []
        vocs_to_exclude = [".", ",", ":", "``", "''", "?", "!", "...", "[", "]"]
        id_ = 1
        for sub in subs:
            morph = nltk.word_tokenize(sub.sentence)
            voc_pos_list = nltk.pos_tag(morph)
            for voc, pos in voc_pos_list:
                if voc in vocs_to_exclude:
                    continue
                vocabulary = Vocabulary(id=id_,
                                        english=voc.lower(),
                                        pos=pos,
                                        subject_id=sub.id)
                vocabularies.append(vocabulary)
                id_ += 1
        return vocabularies

    @exception_module
    def write_csv(self, freqs: list[Vocabulary, ], output_path: str | None = None) -> None:
        if output_path:
            path = self.csv_repo.path
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(freqs, path=output_path)

    @exception_module
    def write_gss(self, freqs: list[Vocabulary, ]) -> None:
        self.gss_repo.add(freqs)

    @exception_module
    def add_by_pos(self, vocabs: list[Vocabulary, ]) -> None:
        poss = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS",
                "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS",
                "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO",
                "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
                "WP", "WP$", "WRB"]
        for pos in poss:
            output_path = f"/pos/{pos}"
            vocabs_pos = self.__extract_by_pos(vocabs, pos)
            self.write_csv(vocabs_pos, output_path=output_path)

    @staticmethod
    def __extract_by_pos(vocabularies: list[Vocabulary,], pos: str) -> list[Vocabulary,]:
        vocabs_pos = []
        for vocab in vocabularies:
            if vocab.pos == pos:
                vocabs_pos.append(vocab)

        return vocabs_pos
