import xlsxwriter
import os
from django.conf import settings
from .models import Table


def check_extension(file_name):
    extension = file_name.split('.')[-1]
    if extension == 'xls':
        return file_name
    else:
        return file_name+'.xls'


def export_in_xls(publications, file_name):
    file_name = check_extension(file_name)
    workbook = xlsxwriter.Workbook(os.path.join(settings.MEDIA_ROOT, f'{file_name}'))
    worksheet = workbook.add_worksheet()
    headers = ['Название', 'Издание', 'Год публикации', 'Тип публикации',
               'Диапазон', 'Номер УК']

    col = 0
    for name in headers:
        worksheet.write(0, col, name)
        col += 1

    row = 1
    for publication in publications:
        col = 0
        worksheet.write(row, col, publication.title)
        worksheet.write(row, col + 1, publication.edition)
        worksheet.write(row, col + 2, publication.published_year)
        if publication.type_of_publication is None:
            worksheet.write(row, col + 3, '')
        else:
            worksheet.write(row, col + 3, publication.type_of_publication.type_of_publication)
        worksheet.write(row, col + 4, publication.range)
        worksheet.write(row, col + 5, publication.uk_number)
        row += 1
    workbook.close()
    file = Table.objects.create(file=f'{file_name}')
    return file
