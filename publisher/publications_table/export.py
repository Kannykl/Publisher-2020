import xlsxwriter


def export_in_xls(publications, file_name):
    workbook = xlsxwriter.Workbook(f'{file_name}')
    worksheet = workbook.add_worksheet()
    headers = ['Звание', 'ФИО', 'Должность', 'Название', 'Издание', 'Год публикации', 'Тип публикации',
               'Диапазон', 'Номер УК']

    col = 0
    for name in headers:
        worksheet.write(0, col, name)
        col += 1

    row = 1
    for publication in publications:
        for author in publication.authors.all():
            col = 0
            worksheet.write(row, col, author.military_rank)
            initials = author.surname + ' ' + author.name[:1] + '.' + author.patronymic[:1] + '.'
            worksheet.write(row, col + 1, initials)
            worksheet.write(row, col + 2, author.work_position)
            worksheet.write(row, col + 3, publication.title)
            worksheet.write(row, col + 4, publication.edition)
            worksheet.write(row, col + 5, publication.published_year)
            worksheet.write(row, col + 6, publication.type_of_publication)
            worksheet.write(row, col + 7, publication.range)
            worksheet.write(row, col + 8, publication.uk_number)
            row += 1
    workbook.close()
