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
from models import Model


@dataclass
class Vocabulary(Model):
    """vocabulary data class"""
    id: int | None = field(init=True, default=None)
    english: str | None = field(init=True, default=None)
    pos: str | None = field(init=True, default=None)
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
            "pos": dict_.get("pos"),
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
            "pos": self.pos,
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
