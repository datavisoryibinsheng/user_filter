import openpyxl
import csv


def read_xlsx(path, header=None):
    """
    :param path: xlsx file path
    :return:
    """
    wb = openpyxl.open(path)
    ws = wb.get_active_sheet()
    ret = []
    cnt = 0
    for row in ws.rows:
        cnt += 1
        if cnt == 1 and header is None:
            header = [cell.value for cell in row]
            continue
        if len(header) != len(row):
            print('line {} not match schema in file {}!'.format(cnt, path))
            continue
        tmp = {}
        for k, cell in zip(header, row):
            if cell.value is not None:
                v = cell.value
            else:
                v = ''
            tmp[k] = v
        ret.append(tmp)
    return ret


def load_data_from_csv(path):
    ret = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            tmp = dict(list(zip(header, row)))
            ret.append(tmp)
    return header, ret


def write_csv_to_file(path, header, data):
    with open(path, 'w', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    z = read_xlsx(path='tmp/dv_input/client/test.xlsx')
    print(z[:5])
    header, z = load_data_from_csv(path='tmp/dv_input/dv/test.csv')
    print(header)
    print(z[:5])
    write_csv_to_file('tmp/dv_output/output.txt', header, z)