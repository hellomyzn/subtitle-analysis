"""repositories.group_preposition.gss_group_preposition_repository"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from repositories.vocabularies import GssVocabularyRepository


class GssGroupPrepositionRepository(GssVocabularyRepository):
    """gss group preposition repository"""

    def __init__(self):
        super().__init__(sheet_name="group preposition")
