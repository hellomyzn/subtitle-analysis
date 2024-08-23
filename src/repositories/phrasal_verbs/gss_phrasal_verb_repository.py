"""repositories.phrasal_verb.gss_vocabulary_repository"""
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


class GssPhrasalVerbRepository(GssVocabularyRepository):
    """gss phrasal verb repository"""

    def __init__(self):
        super().__init__(sheet_name="phrasal verb")
