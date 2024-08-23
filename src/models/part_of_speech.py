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
from common.log import warn


@dataclass
class PartOfSpeech(Model):
    """part of speech data class"""
    CC: list = field(init=True, default_factory=list)
    CD: list = field(init=True, default_factory=list)
    DT: list = field(init=True, default_factory=list)
    EX: list = field(init=True, default_factory=list)
    FW: list = field(init=True, default_factory=list)
    IN: list = field(init=True, default_factory=list)
    JJ: list = field(init=True, default_factory=list)
    JJR: list = field(init=True, default_factory=list)
    JJS: list = field(init=True, default_factory=list)
    LS: list = field(init=True, default_factory=list)
    MD: list = field(init=True, default_factory=list)
    NN: list = field(init=True, default_factory=list)
    NNS: list = field(init=True, default_factory=list)
    NNP: list = field(init=True, default_factory=list)
    NNPS: list = field(init=True, default_factory=list)
    PDT: list = field(init=True, default_factory=list)
    POS: list = field(init=True, default_factory=list)
    PRP: list = field(init=True, default_factory=list)
    PRP_DOLLAR: list = field(init=True, default_factory=list)
    RB: list = field(init=True, default_factory=list)
    RBR: list = field(init=True, default_factory=list)
    RBS: list = field(init=True, default_factory=list)
    RP: list = field(init=True, default_factory=list)
    SYM: list = field(init=True, default_factory=list)
    TO: list = field(init=True, default_factory=list)
    UH: list = field(init=True, default_factory=list)
    VB: list = field(init=True, default_factory=list)
    VBD: list = field(init=True, default_factory=list)
    VBG: list = field(init=True, default_factory=list)
    VBN: list = field(init=True, default_factory=list)
    VBP: list = field(init=True, default_factory=list)
    VBZ: list = field(init=True, default_factory=list)
    WDT: list = field(init=True, default_factory=list)
    WP: list = field(init=True, default_factory=list)
    WP_DOLLAR: list = field(init=True, default_factory=list)
    WRB: list = field(init=True, default_factory=list)
    _DOLLAR: list = field(init=True, default_factory=list)
    VPV: list = field(init=True, default_factory=list)
    GP: list = field(init=True, default_factory=list)

    attributes = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS",
                  "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS",
                  "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO",
                  "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
                  "WP", "WP$", "WRB", "$", "VPV", "GP"]

    verbs_keys = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    adjectives_keys = ["JJ", "JJR", "JJS"]
    adverbs_keys = ["RB", "RBR", "RBS", "RP"]
    nouns_keys = ["NN", "NNS"]

    @classmethod
    def from_dict(cls, dict_: dict):
        """convert from dict to model

        Args:
            dict_ (dict): dict data

        Returns:
            Sample: model
        """
        return cls(**{
            "CC": dict_.get("CC"),
            "CD": dict_.get("CD"),
            "DT": dict_.get("DT"),
            "EX": dict_.get("EX"),
            "FW": dict_.get("FW"),
            "IN": dict_.get("IN"),
            "JJ": dict_.get("JJ"),
            "JJR": dict_.get("JJR"),
            "JJS": dict_.get("JJS"),
            "LS": dict_.get("LS"),
            "MD": dict_.get("MD"),
            "NN": dict_.get("NN"),
            "NNS": dict_.get("NNS"),
            "NNP": dict_.get("NNP"),
            "NNPS": dict_.get("NNPS"),
            "PDT": dict_.get("PDT"),
            "POS": dict_.get("POS"),
            "PRP": dict_.get("PRP"),
            "PRP_DOLLAR": dict_.get("PRP$"),
            "RB": dict_.get("RB"),
            "RBR": dict_.get("RBR"),
            "RBS": dict_.get("RBS"),
            "RP": dict_.get("RP"),
            "SYM": dict_.get("SYM"),
            "TO": dict_.get("TO"),
            "UH": dict_.get("UH"),
            "VB": dict_.get("VB"),
            "VBD": dict_.get("VBD"),
            "VBG": dict_.get("VBG"),
            "VBN": dict_.get("VBN"),
            "VBP": dict_.get("VBP"),
            "VBZ": dict_.get("VBZ"),
            "WDT": dict_.get("WDT"),
            "WP": dict_.get("WP"),
            "WP_DOLLAR": dict_.get("WP$"),
            "WRB": dict_.get("WRB"),
            "_DOLLAR": dict_.get("$"),
            "VPV": dict_.get("VPV"),
            "GP": dict_.get("GP")})

    def to_dict(self, without_none_field: bool = False) -> dict:
        """convert from model to dict

        Args:
            without_none_field (bool, optional): option to remove none fields. Defaults to False.

        Returns:
            dict: dict data
        """
        dict_ = {
            "CC": self.CC,
            "CD": self.CD,
            "DT": self.DT,
            "EX": self.EX,
            "FW": self.FW,
            "IN": self.IN,
            "JJ": self.JJ,
            "JJR": self.JJR,
            "JJS": self.JJS,
            "LS": self.LS,
            "MD": self.MD,
            "NN": self.NN,
            "NNS": self.NNS,
            "NNP": self.NNP,
            "NNPS": self.NNPS,
            "PDT": self.PDT,
            "POS": self.POS,
            "PRP": self.PRP,
            "PRP$": self.PRP_DOLLAR,
            "RB": self.RB,
            "RBR": self.RBR,
            "RBS": self.RBS,
            "RP": self.RP,
            "SYM": self.SYM,
            "TO": self.TO,
            "UH": self.UH,
            "VB": self.VB,
            "VBD": self.VBD,
            "VBG": self.VBG,
            "VBN": self.VBN,
            "VBP": self.VBP,
            "VBZ": self.VBZ,
            "WDT": self.WDT,
            "WP": self.WP,
            "WP$": self.WP_DOLLAR,
            "WRB": self.WRB,
            "$": self._DOLLAR,
            "VPV": self.VPV,
            "GP": self.GP}

        if without_none_field:
            return {key: value for key, value in dict_.items() if value is not None}

        return dict_

    def to_json(self) -> str:
        """convert from model to json

        Returns:
            json: json data
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def get_values(self, pos: str) -> list:
        """$(DOLLAR)の付く変数名があるため、パースする

        Args:
            pos (str): _description_

        Returns:
            list: _description_
        """
        if "$" in pos:
            pos = pos.replace("$", "_DOLLAR")
        try:
            return getattr(self, pos)
        except AttributeError as exc:
            warn("{0}", exc)

    def append_values(self, pos: str, vocab: str) -> None:
        if "$" in pos:
            pos = pos.replace("$", "_DOLLAR")
        try:
            getattr(self, pos).append(vocab)
        except AttributeError as exc:
            warn("{0}", exc)
