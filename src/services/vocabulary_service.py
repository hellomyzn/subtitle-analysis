"""services.vocabulary_service"""
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
from common.log import info
from models import Subtitle
from models import Vocabulary
from models import PartOfSpeech
from repositories.vocabularies import CsvVocabularyRepository
from repositories.vocabularies import GssVocabularyRepository
from utils import (has_file,
                   make_file,
                   lemmatize_vocabulary,
                   word_tokenize,
                   pos_tag,
                   scrap_vocabulary)


@ dataclass
class VocabularyService(object):
    """vocabulary service"""

    def __init__(self):
        self.csv_repo = CsvVocabularyRepository()
        self.gss_repo = GssVocabularyRepository()

    @ exception_module
    def add(self, vocabs: list[Vocabulary, ]):
        """
        Adds a list of Vocabulary objects by writing them to both a CSV file and Google Sheets.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to be added.
        """
        self.write_csv(vocabs)
        self.write_gss(vocabs)

    @ exception_module
    def extract_from_subtitles(self, subs: list[Subtitle, ]):
        """
        Extracts vocabulary from subtitles using the NLTK package.

        Args:
            subs (list[Subtitle]): A list of English subtitles.

        Returns:
            list[Vocabulary]: A list of Vocabulary objects created from the subtitles.
        """
        info("extract vocabularies from subtitles")
        vocabularies = []
        vocs_to_exclude = [".", ",", ":", "``", "''", "?", "!", "...", "[", "]", "&"]
        id_ = 1

        for sub in subs:
            # Tokenize the sentence into words
            words = word_tokenize(sub.sentence)
            # Tag each word with its part of speech
            tagged_words = pos_tag(words)

            for word, pos in tagged_words:
                word = word.lower()

                # Skip excluded vocabulary
                if word in vocs_to_exclude:
                    continue

                vocabulary = Vocabulary(
                    id=id_,
                    word=word,
                    meaning=None,
                    pos=pos,
                    original_form=None,
                    level=None,
                    eiken_level=None,
                    school_level=None,
                    toeic_level=None,
                    subtitle_id=sub.id)

                # Lemmatize to get the original form (e.g., studied -> study)
                origin = lemmatize_vocabulary(vocabulary)
                vocabulary.original_form = origin

                # Avoid scraping the same vocabulary by checking if it already exists
                existing_vocab = vocabulary.find_by_attr(vocabularies, "word")

                if existing_vocab:
                    vocabulary.level = existing_vocab.level
                    vocabulary.eiken_level = existing_vocab.eiken_level
                    vocabulary.school_level = existing_vocab.school_level
                    vocabulary.toeic_level = existing_vocab.toeic_level
                    vocabulary.meaning = existing_vocab.meaning
                else:
                    vocabulary.level, vocabulary.eiken_level, vocabulary.school_level, vocabulary.toeic_level, vocabulary.meaning = scrap_vocabulary(
                        vocabulary)
                info(vocabulary)

                vocabularies.append(vocabulary)
                id_ += 1

        info("extracted vocabularies: {0}", len(vocabularies))
        return vocabularies

    @ exception_module
    def write_csv(self, vocabs: list[Vocabulary, ], output_path: str | None = None) -> None:
        """
        Writes a list of Vocabulary objects to a CSV file.
        If an output path is provided, the CSV will be saved to that location with a modified filename.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to write to the CSV file.
            output_path (str | None): Optional; If provided, this path will be used for the output CSV file.

        Returns:
            None
        """
        path = self.csv_repo.path

        if output_path:
            dir_path = "/".join(path.split("/")[:-1])
            filename = f"{output_path}_{path.split('/')[-1]}"
            output_path = f"{dir_path}/{filename}"

            if not has_file(output_path):
                make_file(output_path)

        self.csv_repo.write(vocabs, path=output_path)

    @ exception_module
    def write_gss(self, vocabs: list[Vocabulary, ]) -> None:
        """
        Writes a list of Vocabulary objects to Google Sheets.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to add to Google Sheets.

        Returns:
            None
        """
        self.gss_repo.add(vocabs)

    @ exception_module
    def sort_by_pos(self, vocabs: list[Vocabulary, ]) -> PartOfSpeech:
        """
        Sorts a list of Vocabulary objects by their part of speech and groups them into a PartOfSpeech object.

        Args:
            vocabs (list[Vocabulary]): The list of Vocabulary objects to sort.

        Returns:
            PartOfSpeech: An object containing the grouped Vocabulary objects by their part of speech.
        """
        info("sort vocabularies by part of speech")
        pos = PartOfSpeech()
        for vocab in vocabs:
            pos.append_values(vocab.pos, vocab)
        info("sorted vocabularies by part of speech")
        return pos

    @ exception_module
    def add_by_pos(self, part_of_speech: PartOfSpeech) -> None:
        """
        Adds Vocabulary objects grouped by their part of speech to CSV files.

        Args:
            part_of_speech (PartOfSpeech): An object containing Vocabulary objects grouped by part of speech.

        Returns:
            None
        """
        for pos in part_of_speech.attributes:
            vocabs = part_of_speech.get_values(pos)
            output_path = f"/pos/{pos}"
            self.write_csv(vocabs, output_path=output_path)
