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
class Frequency(Model):
    """vocabulary data class"""
    id: int | None = field(init=True, default=None)
    vocabulary: str | None = field(init=True, default=None)
    times: int | None = field(init=True, default=None)
    level: str | None = field(init=True, default=None)
    eiken_level: str | None = field(init=True, default=None)
    school_level: str | None = field(init=True, default=None)
    toeic_level: str | None = field(init=True, default=None)

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
            "vocabulary": dict_.get("vocabulary"),
            "times": dict_.get("times"),
            "level": dict_.get("level"),
            "eiken_level": dict_.get("eiken_level"),
            "school_level": dict_.get("school_level"),
            "toeic_level": dict_.get("toeic_level")
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
            "vocabulary": self.vocabulary,
            "times": self.times,
            "level": self.level,
            "eiken_level": self.eiken_level,
            "school_level": self.school_level,
            "toeic_level": self.toeic_level
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
