from pathlib import Path

from pymystem3 import Mystem
from json import dumps


def read_text_file(path:Path) -> str:
    result = ''
    with path.open(encoding='utf-8') as f:
        result = f.read()
    return result


def lemmas_and_map_stat():
    # потребуется удалить переносы строк
    pass


mystem = Mystem()

if __name__ == '__main__':
    text = read_text_file(Path('HP1RUS_PART1.txt'))
    lemmas: list[str] = mystem.lemmatize(text) # отсюда берем леммы
    analysis_result = mystem.analyze(text) # список словарей, в каждом элементе analysis - список словарей свойств, text - исходное слово
    # по сути все что надо - извлечь часть речи
    # замечание, у знаков препинания нет ключа analysis, он есть только у осмысленных слов
    print(lemmas)
    print(analysis_result)
    print("lemmas:", ''.join(lemmas))
    print("full info:", dumps(analysis_result, ensure_ascii=False))