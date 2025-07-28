from argparse import ArgumentParser, ArgumentTypeError
from enum import StrEnum
from logging import getLogger, basicConfig, INFO, DEBUG
from pathlib import Path

from reports import save_report
from text_preprocessing import read_and_assemble_sentences
from text_processing import extract_lemmas_from_sentences


logger = getLogger(__name__)
basicConfig(level=INFO)


PART_OF_SPEECH = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V']


class SortType(StrEnum):
    alphabetic = "alphabetic"
    alphabetic_reverse = "alphabetic-reverse"
    frequency = "frequency"
    frequency_reverse = "frequency-reverse"


def process_text_files(file_paths: list[Path], exclude_proper_names: bool = False, sort_type: SortType = SortType.alphabetic,
                       exclude_pos=None):
    if exclude_pos is None:
        exclude_pos = list()
    text_vectors = []
    for file_path in file_paths:
        logger.info(f'Обработка {file_path.stem}')
        sentences = read_and_assemble_sentences(file_path)
        result_vector = extract_lemmas_from_sentences(sentences, exclude_proper_names, exclude_pos)
        text_vectors.append(result_vector)
    text_vectors = normalize_text_vectors(text_vectors, sort_type)
    save_report(text_vectors, file_paths)


def normalize_text_vectors(text_vectors: list[dict[tuple[str,str],int]], sort_type: SortType):
    """
    Приводим вектора текстов к одной длине, если слово отсутствует в тексте его частота приравнивается к нулю
    :param text_vectors: Список словарей частот для одного или нескольких текстов
    :param sort_type: Сортировка словарей, по умолчанию применяется сортировка по алфавиту
    :return: Список частотных словарей, длины которых были скорректированы
    """
    logger.info('Нормализация словарей')
    result = list()
    all_keys = []
    for text_vector in text_vectors:
        all_keys.extend(text_vector.keys())
    for text_vector in text_vectors:
        for key in all_keys:
            if key not in text_vector:
                text_vector[key] = 0
        sorted_dict = None
        if sort_type == SortType.alphabetic:
            sorted_dict = dict(sorted(text_vector.items()))
        elif sort_type == SortType.alphabetic_reverse:
            sorted_dict = dict(sorted(text_vector.items(),reverse=True))
        elif sort_type == SortType.frequency:
            sorted_dict = dict(sorted(text_vector.items(), key=lambda item: item[1]))
        elif sort_type == SortType.frequency_reverse:
            sorted_dict = dict(sorted(text_vector.items(), key=lambda item: item[1], reverse=True))
        else:
            sorted_dict = dict(sorted(text_vector.items()))
        result.append(sorted_dict)
    return result


if __name__ == '__main__':
    parser = ArgumentParser(
        prog='MystemWrapper',
        usage='python main.py --texts [PATH_TO_FILE] [PATH_TO_FILE] [OPTION]',
        description='Программа для подсчета частот одного или нескольких текстов'
    )
    parser.add_argument(
        '-t',
        '--texts',
        nargs='*',
        type=Path,
        required=True,
        help='Путь до файлов текста в формате ".txt". Например, --texts C:\\Users\\Miroslav\\file1.txt',
    )
    parser.add_argument(
        '-e',
        '--exclude-proper-names',
        action='store_true',
        help='Исключить из подсчета имена собственные.'
    )
    parser.add_argument(
        '-s',
        '--sort',
        type=SortType,
        choices=list(SortType),
        default=SortType.alphabetic,
        help='Сортировка по алфавиту (alphabetic, alphabetic-reverse) или частоте (frequency, frequency-reverse). '
             'По умолчанию применяется сортировка по алфавиту (--sort alphabetic).'
    )
    parser.add_argument(
        '-ep',
        '--exclude-pos',
        nargs='*',
        type=str,
        choices=PART_OF_SPEECH,
        help='Исключить из подсчета отдельные части речи. '
             'Например --exclude-pos PART PR для исключения частиц и предлогов.'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Отладочная информация выводится в консоль.'
    )

    args = parser.parse_args()
    if args.debug:
        basicConfig(level=DEBUG)
    if len(args.texts) > 0:
        if len(args.texts) > 1 and args.sort != SortType.alphabetic:
            logger.warning('На одинаковых местах в итоговых векторах будут стоять разные слова (из-за разных частот)!')

        missing = [p for p in args.texts if not p.is_file()]
        if missing:
            parser.error(f'Файлы не найдены: {", ".join(map(str, missing))}')

        process_text_files(args.texts, args.exclude_proper_names, args.sort, args.exclude_pos)
    else:
        logger.info('Для работы программы необходим хотя бы текстовый файл')
        logger.info('Добавить путь к файлу можно через аргумент --texts')
        logger.info('Например, --texts C:\\Users\\Miroslav\\file1.txt')
        logger.info('Для нескольких текстов, --texts C:\\Users\\Miroslav\\file1.txt C:\\Users\\Miroslav\\file2.txt')
