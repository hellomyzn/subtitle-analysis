"""models.vocabulary"""
#########################################################
# Builtin packages
#########################################################
import json
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from models import Model, Subtitle
from repositories.subtitles import CsvSubtitleRepository


@dataclass
class Vocabulary(Model):
    """vocabulary data class"""
    id: int | None = field(init=True, default=None)
    english: str | None = field(init=True, default=None)
    meaning: str | None = field(init=True, default=None)
    pos: str | None = field(init=True, default=None)
    original: str | None = field(init=True, default=None)
    level: str | None = field(init=True, default=None)
    eiken_level: str | None = field(init=True, default=None)
    school_level: str | None = field(init=True, default=None)
    toeic_level: str | None = field(init=True, default=None)
    subject_id: str | None = field(init=True, default=None)

    @classmethod
    def from_dict(cls, dict_: dict):
        """convert from dict to model

        Args:
            dict_ (dict): dict data

        Returns:
            Sample: model
        """
        return cls(**{
            "id": dict_.get("id"),
            "english": dict_.get("english"),
            "meaning": dict_.get("meaning"),
            "pos": dict_.get("pos"),
            "original": dict_.get("original"),
            "level": dict_.get("level"),
            "eiken_level": dict_.get("eiken_level"),
            "school_level": dict_.get("school_level"),
            "toeic_level": dict_.get("toeic_level"),
            "subject_id": dict_.get("subject_id")
        })

    def to_dict(self, without_none_field: bool = False) -> dict:
        """convert from model to dict

        Args:
            without_none_field (bool, optional): option to remove none fields. Defaults to False.

        Returns:
            dict: dict data
        """
        dict_ = {
            "id": self.id,
            "english": self.english,
            "meaning": self.meaning,
            "pos": self.pos,
            "original": self.original,
            "level": self.level,
            "eiken_level": self.eiken_level,
            "school_level": self.school_level,
            "toeic_level": self.toeic_level,
            "subject_id": self.subject_id
        }

        if without_none_field:
            return {key: value for key, value in dict_.items() if value is not None}

        return dict_

    def to_json(self) -> str:
        """convert from model to json

        Returns:
            json: json data
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def fetch_subtitle(self) -> Subtitle:
        """
        Retrieves the subtitle associated with the object's subject ID.

        Returns:
            Subtitle: The subtitle corresponding to the object's subject ID, retrieved from the CSV subtitle repository.
        """
        csv_subtitle = CsvSubtitleRepository()
        return csv_subtitle.find_by_id(self.subject_id)

    def find_by_attr(self, vocabs: list["Vocabulary", ], attr: str):
        """
        Searches for an object in the list with the same attribute value as the calling object.

        Args:
            vocabs (list["Vocabulary"]): A list of Vocabulary objects to search through.
            attr (str): The attribute name to compare between the calling object and the list elements.

        Returns:
            Vocabulary or None: The first Vocabulary object from the list that has the same value
            for the specified attribute as the calling object. Returns None if no match is found.
        """

        value_to_find = getattr(self, attr)

        for vocab in vocabs:
            if getattr(vocab, attr) == value_to_find:
                return vocab
        return None

    def is_coordinating_conjunction(self) -> bool:
        """check coordinating conjunction

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        return self.pos in ["CC"]

    def is_existential_there(self) -> bool:
        """check existential there

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        return self.pos in ["EX"]

    def is_verb(self) -> bool:
        """check verb

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        return self.pos in verbs

    def is_preposition(self) -> bool:
        """check preposition

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        preposition = ["IN", "RP", "TO"]

        return self.pos in preposition

    def is_adverb(self) -> bool:
        """check verb

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        adverbs = ["RB", "RBR", "RBS", "RP"]
        return self.pos in adverbs

    def is_adjective(self) -> bool:
        """check verb

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        adjective = ["JJ", "JJR", "JJS"]
        return self.pos in adjective

    def is_conjunction(self) -> bool:
        """check conjunction

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        adjective = ["CC", "IN"]
        return self.pos in adjective

    def is_noun(self) -> bool:
        """check noun

        Args:
            vocab (Vocabulary): vocabulary to check

        Returns:
            bool: True or False
        """
        adjective = ["NN", "NNS"]
        return self.pos in adjective
