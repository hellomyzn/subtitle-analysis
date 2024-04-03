"""services.vocabulary_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass, field

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
from utils import has_file, make_file


@dataclass
class VocabularyService(object):
    """vocabulary service"""

    def __init__(self):
        self.csv_repo = CsvVocabularyRepository()

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
    def extract_by_pos(self, vocabularies: list[Vocabulary,], pos: str) -> list[Vocabulary,]:

        pos_vocabs = []
        for vocab in vocabularies:
            if vocab.pos == pos:
                pos_vocabs.append(vocab)

        return pos_vocabs
