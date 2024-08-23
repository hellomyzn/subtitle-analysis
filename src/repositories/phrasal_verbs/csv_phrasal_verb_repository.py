"""repositories.vocabularies.csv_phrasal_verb_repository"""
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
from common.config import PHRASAL_VERB_PATH, TARGET_PATH
from repositories.vocabularies import CsvVocabularyRepository
from utils import has_file, make_file


class CsvPhrasalVerbRepository(CsvVocabularyRepository):
    """csv phrasal verb repository"""

    def __init__(self):
        super().__init__()
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        self.path = f"{PHRASAL_VERB_PATH}/phrasal_verb_{file_name}{extension}"
        # not write csv since it's written on pos/VPV
        # if not has_file(self.path):
        #     make_file(self.path)
