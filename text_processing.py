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
    # chunk_size = 1
    logger.info(f'Размер чанка предложений {chunk_size}')
    # chunk_size = max(1, int(log(max(len(sentences), 1), e)))
    result_vector = Counter()
    # result_vector = dict()
    for i in range(0, len(sentences), chunk_size):
        sentence_chunk = ' '.join(sentences[i:i + chunk_size])
        temp_result = get_lemmas_from_sentence_chunk(sentence_chunk, exclude_proper_names, exclude_pos)
        result_vector.update(temp_result)
        # result_vector[sentence_chunk] = temp_result
        logger.info(f'Обработано предложений {min(i + chunk_size, len(sentences))}/{len(sentences)}')
    return dict(result_vector)
    # return result_vector


def get_lemmas_from_sentence_chunk(sentence_chunk: str, exclude_proper_names: bool = False, exclude_pos = None) -> dict[tuple[str,str],int]:
    if exclude_pos is None:
        exclude_pos = list()
    temp_result = {}
    lemmas: list[str] = mystem.lemmatize(sentence_chunk)
    analysis_results = mystem.analyze(sentence_chunk)

    for lemma, analysis_result in zip(lemmas, analysis_results):
        # if not word_regex.match(lemma):
        #     continue
        # у знаков препинания нет ключа analysis + пропускаем если гипотез нет
        if 'analysis' not in analysis_result or len(analysis_result['analysis']) == 0:
            continue
        # гипотез может быть несколько, берем первую
        hypothesis = analysis_result['analysis'][0]
        part_of_speech, is_proper_name = get_word_properties(hypothesis)
        # исключаем из расчетов имена собственные и отдельные части речи
        if is_proper_name and exclude_proper_names or part_of_speech in exclude_pos:
            continue
        key = (lemma, part_of_speech)
        if key not in temp_result:
            temp_result[key] = 0
        temp_result[key] += 1
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


# if __name__ == '__main__':
#     text = 'И Марья Николаевна целовала, смеялась, тормошила ее, и обе они валялись и путались в белых простынях, полуголые -- одна гибкая, сильная и упругая, другая тоненькая и хрупкая, -- как две расшалившиеся дикие прекрасные самочки какого-то сильного счастливого зверя. XIV В этот день Семенов с дневным поездом уезжал в Ялту, где было, как говорили доктора, которым он не верил, но хотел верить, его спасение. Все собрались его проводить. Семенов чувствовал себя очень плохо. Его уже не веселили ни солнце, ни тепло, ни люди, ни небо, ни зелень. Ноющее, бесконечное страдание наполняло и окружало его, как какой-то особый тяжелый туман, сквозь который плохо и тускло видел он все окружающее. Он уезжал равнодушный и холодный, как будто тело его уже умерло, а дух был погружен куда-то внутрь, в бездонную глубину одинокою страдания. Он не был рад, но и не раздражался, оттого что его собрались провожать. Ему было все равно. Один Ланде его заботил, и так странно было видеть это непонятное, озабоченное внимание, как улыбку на лице неподвижного холодного покойника. -- Ты, Ланде, оставайся и живи тут! -- сухо покашливая, говорил он. -- А что же ты есть будешь? -- Как-нибудь... -- улыбаясь, успокаивал его Ланде и, шутя, прибавлял: -- Взгляните на птиц небесных: не сеют... -- Ты дурак! -- сердито возразил Семенов: -- ты не птица... Ведь тебя не накорми, так ты с голода подохнешь. Удивительное дело!.. На месте Господа Бога я бы тебя давно взял живым... и посадил в сумасшедший дом. Ланде смеялся заразительно весело и добродушно. Милый Вася, ты лучше всех людей, каких я встречал... -- А ты глупей... -- болезненно и нетерпеливо махнул рукой Семенов. Он помолчал. -- Шишмарев обещал тебе урок достать. Ну, вот и хорошо! -- обрадовался Ланде. -- Только это очень трудно: ты ведь уже на весь город прославился... Пришли Шишмарев и Молочаев. -- Едете? -- безразлично спросил художник. -- Конечно! -- с тусклой неприязнью ответил Семенов. -- Урок для Ланде я нашел, -- сказал Шишмарев таким голосом, точно сомневался в чем-то. -- Ну, вот... слышишь? -- посмотрел на Ланде Семенов. -- Скоро пора и на вокзал... -- заметил Шишмарев, озабоченно посмотрев на часы. Когда Семенов вышел куда-то, Молочаев равнодушно сказал: -- Куда он едет? В Ялту? На какие средства? -- На кондицию... -- ответил Шишмарев, пожав плечами. -- Дело студенческое! -- На урок? -- удивился Молочаев, и на минуту тень жалости налетела на его лицо. -- Куда ж ему на урок? Его ветер с ног валит! Ланде встал, схватился за щеку, как от внезапной боли, потом опять сел. -- Э, что! -- сказал Шишмарев, точно ему было даже приятно это сказать, -- нашему брату, голяку, нельзя такими нежностями заниматься! Пока еще не свалил? -- ну, и ладно! Под окном мелькнул черный ажурный зонтик и другой розовый. -- Марья Николаевна и Соня идут! -- сказал Ланде. Они вошли вместе с Семеновым.'
#     print(get_lemmas_from_sentence_chunk(text))