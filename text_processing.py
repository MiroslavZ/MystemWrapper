from collections import Counter
from logging import getLogger
from math import sqrt, log, e
from re import compile, match, UNICODE

from pymystem3 import Mystem


logger = getLogger(__name__)


# "C:\Users\Miroslav\.local\bin\mystem.exe"
mystem = Mystem()
word_regex = compile(r'^[^\W\d_]+(?:-[^\W\d_]+)*$', flags=UNICODE)


def extract_lemmas_from_sentences(sentences: list[str], exclude_proper_names: bool = False, exclude_pos=None) -> dict[tuple[str,str],int]:
    # обработка чанками увеличивает время, но позволяет контролировать прогресс
    if exclude_pos is None:
        exclude_pos = list()
    chunk_size = max(1, int(sqrt(len(sentences))))
    logger.info(f'Размер чанка предложений {chunk_size}')
    # chunk_size = max(1, int(log(max(len(sentences), 1), e)))
    result_vector = Counter()
    for i in range(0, len(sentences), chunk_size):
        sentence_chunk = '. '.join(sentences[i:i + chunk_size])
        temp_result = get_lemmas_from_sentence_chunk(sentence_chunk, exclude_proper_names, exclude_pos)
        result_vector.update(temp_result)
        logger.info(f'Обработано предложений {min(i + chunk_size, len(sentences))}/{len(sentences)}')
    return dict(result_vector)


def get_lemmas_from_sentence_chunk(sentence_chunk: str, exclude_proper_names: bool = False, exclude_pos = None) -> dict[tuple[str,str],int]:
    if exclude_pos is None:
        exclude_pos = list()
    temp_result = {}
    lemmas: list[str] = mystem.lemmatize(sentence_chunk)
    analysis_results = mystem.analyze(sentence_chunk)
    start_index = 0
    for lemma in lemmas:
        is_word = word_regex.match(lemma)
        if not is_word:
            continue
        analysis_for_lemma_founded = False
        for idx in range(start_index,len(analysis_results)):
            analysis_result = analysis_results[idx]
            if 'analysis' in analysis_result:  # у знаков препинания нет такого ключа
                # гипотез может быть несколько, берем первую, гипотез может и не быть!
                if len(analysis_result['analysis']) == 0:
                    continue
                hypothesis = analysis_result['analysis'][0]
                if hypothesis['lex'] == lemma:
                    part_of_speech, is_proper_name = get_word_properties(hypothesis)
                    analysis_for_lemma_founded = True
                    if is_proper_name and exclude_proper_names or part_of_speech in exclude_pos:
                        # исключаем из расчетов имена собственные и отдельные части речи
                        break
                    key = (lemma, part_of_speech)
                    if key not in temp_result:
                        temp_result[key] = 0
                    temp_result[key] += 1
                else:
                    pass
            start_index = idx
            if analysis_for_lemma_founded:
                break
    return temp_result


def get_word_properties(hypothesis:dict) -> tuple[str, bool]:
    """
    Упрощенное получение свойств слова
    :param hypothesis: словарь гипотезы mystem
    :return: строковое представление части речи в mystem и флаг является ли слово именем собственным
    """
    # Пример: 'S,имя,муж,од=(пр,мн|пр,ед|вин,мн|вин,ед|дат,мн)'
    properties:str = hypothesis['gr']
    start, end = match(r'\w+', properties).span()
    raw_part_of_speech = properties[start:end]
    is_proper_name = False
    if len(properties) > end and properties[end] == ',':
        splitted_props = properties.split(',')
        if len(splitted_props) > 1 and splitted_props[1] == 'имя':
            is_proper_name = True
    return raw_part_of_speech, is_proper_name
