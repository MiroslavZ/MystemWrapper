from datetime import datetime
from logging import getLogger
from pathlib import Path

from openpyxl import Workbook


logger = getLogger(__name__)


def save_report(result_vectors: list[dict[tuple[str, str], int]], original_files: list[Path]) -> None:
    logger.info('Создание отчета')
    workbook = Workbook()
    worksheet = workbook.active
    current_date = datetime.now()
    for index, vector in enumerate(result_vectors):

        worksheet.append([original_files[index].stem])

        worksheet.append(['Слово'] + [k[0] for k in vector])
        worksheet.append(['Часть речи'] + [k[1] for k in vector])

        freq_row_start = worksheet.max_row + 1
        worksheet.append(['Частота'] + list(vector.values()))
        freq_row_end = worksheet.max_row
        freq_col_start = 2  # B
        freq_col_end = 1 + len(vector)
        freq_start_cell = worksheet.cell(row=freq_row_start, column=freq_col_start).coordinate
        freq_end_cell = worksheet.cell(row=freq_row_end, column=freq_col_end).coordinate


        freq_sum = sum(vector.values())
        data = ['Доля'] + [round(v / freq_sum, 6) for v in vector.values()]
        share_row_start = worksheet.max_row + 1
        worksheet.append(data)
        share_row_end = worksheet.max_row
        share_col_start = 2
        share_col_end = 1 + len(vector)
        share_start_cell = worksheet.cell(row=share_row_start, column=share_col_start).coordinate
        share_end_cell = worksheet.cell(row=share_row_end, column=share_col_end).coordinate

        worksheet.append(['Частоты', freq_start_cell, freq_end_cell])
        worksheet.append(['Доли', share_start_cell, share_end_cell])
    filename = f'Statistics {current_date.strftime("%Y-%m-%d %H %M %S")}.xlsx'
    workbook.save(filename)
    path = Path(f'./{filename}').resolve()
    logger.info(f'Файл сохранен {path}')
