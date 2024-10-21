"""utils.scraping"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
import bs4

#########################################################
# Own packages
#########################################################
from common.config import Config
from common.log import error
from common.request import get
from models import Vocabulary

CONFIG = Config().config
IS_OFFLINE = CONFIG["APP"]["OFFLINE"]


def scrap_vocabulary(vocab: Vocabulary | str) -> tuple[str | None, str | None, str | None, str | None, str | None]:
    """
        Scrapes Weblio to retrieve vocabulary levels and meaning.

        Args:
            vocab (Vocabulary |str): The vocabulary object containing the word to scrape.

        Returns:
            tuple[str | None, str | None, str | None, str | None, str | None]:
            A tuple containing level, Eiken level, school level, TOEIC level, and meaning.
        """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/78.0.3904.97 Safari/537.36"
        )
    }
    if isinstance(vocab, Vocabulary):
        vocab = vocab.original_form if vocab.original_form else vocab.word
    url = f'https://ejje.weblio.jp/content/{vocab}'

    if IS_OFFLINE:
        return None, None, None, None, "offline mode"
    html = get(url, headers=headers, timeout=60)
    soup = bs4.BeautifulSoup(html.content, "html.parser")
    # Level keys
    level_keys = {
        "レベル": None,
        "英検": None,
        "学校レベル": None,
        "TOEIC® L&Rスコア": None
    }

    # Extract levels
    labels = soup.select(".learning-level-label")
    contents = soup.select(".learning-level-content")
    for label, content in zip(labels, contents):
        label_text = label.text.strip()
        if label_text in level_keys:
            level_keys[label_text] = content.text.strip()
    level = level_keys["レベル"]
    eiken = level_keys["英検"]
    school = level_keys["学校レベル"]
    toeic = level_keys["TOEIC® L&Rスコア"]

    # Extract meaning
    meaning_element = soup.select_one(".content-explanation")
    meaning = meaning_element.text.strip() if meaning_element else None

    return level, eiken, school, toeic, meaning
