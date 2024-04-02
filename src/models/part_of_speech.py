"""models.part of speech"""
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
from models import Model


@dataclass
class PartOfSpeech(Model):
    """part of speech data class"""
    unique_vocab_count: int | None = field(init=True, default=0)
    total_vocab_count: int | None = field(init=True, default=0)
    vocabularies: list | None = field(init=True, default_factory=list)
    frequency: dict | None = field(init=True, default_factory=dict)

    @classmethod
    def from_dict(cls, dict_: dict):
        """convert from dict to model

        Args:
            dict_ (dict): dict data

        Returns:
            Sample: model
        """
        return cls(**{
            "unique_vocab_count": dict_.get("unique_vocab_count"),
            "total_vocab_count": dict_.get("total_vocab_count"),
            "vocabularies": dict_.get("vocabularies"),
            "frequency": dict_.get("frequency")})

    def to_dict(self, without_none_field: bool = False) -> dict:
        """convert from model to dict

        Args:
            without_none_field (bool, optional): option to remove none fields. Defaults to False.

        Returns:
            dict: dict data
        """
        dict_ = {
            "unique_vocab_count": self.unique_vocab_count,
            "total_vocab_count": self.total_vocab_count,
            "vocabularies": self.vocabularies,
            "frequency": self.frequency}

        if without_none_field:
            return {key: value for key, value in dict_.items() if value is not None}

        return dict_

    def to_json(self) -> str:
        """convert from model to json

        Returns:
            json: json data
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
