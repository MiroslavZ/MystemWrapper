from logging import getLogger
from pathlib import Path

from nltk.tokenize import sent_tokenize


logger = getLogger(__name__)


def split_line_to_sentences(line: str) -> list[str]:
    """
    Разделение строки, прочитанной из файла, на предложения.
    Предложение может занимать несколько строк.
    :param line: Строка текста
    :return: Список предложений
    """
    sentences = sent_tokenize(line, language='russian')
    if len(sentences) == 0:
        return sentences
    return [sentence.strip() for sentence in sentences]


def assemble_sentences(parsed_sentences_lists: list[list[str]]) -> list[str]:
    """
    Сборка цельных предложений из ранее обработанных строк текста
    :param parsed_sentences_lists: список списков токенов
    :return: Список предложений
    """
    cache = []
    result = []
    for parsed_sentences_list in parsed_sentences_lists:
        if len(parsed_sentences_list) == 0:
            if len(cache) == 0:
                continue
            assembled_sentence = ' '.join(cache)
            result.append(assembled_sentence)
            cache = []
        for parsed_sentence in parsed_sentences_list:
            if parsed_sentence.endswith(('.', '?', '!')):
                if len(cache) > 0:
                    # если предложение завершено и кэш не пуст - отправляем в кэш и собираем воедино
                    cache.append(parsed_sentence)
                    assembled_sentence = ' '.join(cache)
                    result.append(assembled_sentence)
                    cache = []
                else:
                    # если предложение завершено и кэш пуст - отправляем сразу в результат
                    result.append(parsed_sentence)
                    cache = []
            else:
                # если предложение не завершено - отправляем его в кэш
                cache.append(parsed_sentence)
    return result


def read_file_and_parse_sentences(path:Path) -> list[list[str]]:
    parsed_sentences_lists = []
    with path.open(encoding='utf-8') as f:
        for line in f:
            sentences = split_line_to_sentences(line)
            parsed_sentences_lists.append(sentences)
    return parsed_sentences_lists


def read_and_assemble_sentences(file_path:Path) -> list[str]:
    logger.info('Чтение и сборка списка предложений')
    parsed_sentences_lists = read_file_and_parse_sentences(file_path)
    return assemble_sentences(parsed_sentences_lists)
