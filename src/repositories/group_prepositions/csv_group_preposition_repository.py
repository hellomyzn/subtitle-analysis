"""repositories.group_prepositions.csv_group_preposition_repository"""
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
from common.config import GROUP_PREPOSITION_PATH, TARGET_PATH
from repositories.vocabularies import CsvVocabularyRepository
from utils import has_file, make_file


class CsvGroupPrepositionRepository(CsvVocabularyRepository):
    """csv group_preposition repository"""

    def __init__(self):
        super().__init__()
        file_name = TARGET_PATH.replace("/", "_")
        extension = ".csv"
        self.path = f"{GROUP_PREPOSITION_PATH}/group_preposition_{file_name}{extension}"
        # not write csv since it's written on pos/GP
        # if not has_file(self.path):
        #     make_file(self.path)
