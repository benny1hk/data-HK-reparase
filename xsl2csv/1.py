import xlrd
import csv
import codecs


def csv_from_excel():

    wb = xlrd.open_workbook('overall_rgc.xlsx')
    sh = wb.sheet_by_name('Sheet0')

    # for i, row in enumerate(range(sh.nrows)):
    #     print(i)
        # wr.writerow(sh.row_values(row))


    offset = 1

    rows = []
    for i, row in enumerate(range(sh.nrows)):
        if i <= offset:  # (Optionally) skip headers
            continue
        r = []
        for j, col in enumerate(range(sh.ncols)):
            r.append(sh.cell_value(i, j))
        rows.append(r)

    # print(rows)
    with codecs.open('your_csv_file.csv', 'w', "utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(rows)
        myfile.close()


csv_from_excel()