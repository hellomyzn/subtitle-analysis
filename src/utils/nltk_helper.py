"""utils.nltk_helper"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

#########################################################
# Own packages
#########################################################
# (None)


def word_tokenize(sentence) -> list:
    try:
        return nltk.word_tokenize(sentence)
    except LookupError:
        nltk.download('punkt')
        return nltk.word_tokenize(sentence)


def pos_tag(words: list) -> list:
    try:
        return nltk.pos_tag(words)
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
        return nltk.pos_tag(words)


def lemmatize_vocabulary(vocab) -> str:
    """
    Get the original form (lemma) of the vocabulary.
    For example, 'studied' -> 'study'.
    This works only for verbs, adjectives, adverbs, and nouns.

    Args:
        vocab (Vocabulary): The vocabulary object containing the word to lemmatize.

    Returns:
        str: The original (lemmatized) form of the vocabulary, or the word itself if no lemmatization is possible.
    """
    lem = WordNetLemmatizer()
    word = vocab.word
    pos_map = {
        "v": vocab.is_verb,
        "a": vocab.is_adjective,
        "r": vocab.is_adverb,
        "n": vocab.is_noun
    }

    for mode, check_func in pos_map.items():
        if check_func():
            try:
                return lem.lemmatize(word, mode)
            except LookupError:
                nltk.download('wordnet')
                return lem.lemmatize(word, mode)

    return word
