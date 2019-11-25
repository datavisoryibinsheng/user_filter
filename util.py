import csv
import json
import openpyxl


def load_data_from_xlsx(path, header=None):
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
    return header, ret


def load_data_from_csv(path):
    ret = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            tmp = dict(list(zip(header, row)))
            ret.append(tmp)
    return header, ret


def load_data_from_json(path):
    ret = []
    header = set()
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp.readlines():
            row = json.loads(line)
            header.add(**row.keys())
            ret.append(row)
    return list(header), ret


def write_json_to_file(path, data):
    with open(path, 'w', encoding='utf-8') as fp:
        for row in data:
            fp.write(json.dumps(row, ensure_ascii=False))
            fp.write('\n')


def write_csv_to_file(path, header, data):
    data = [{k: v for k, v in row.items() if k in header} for row in data]
    with open(path, 'w', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def uniform_read(path: str):
    """
    read json, csv, xlsx dict file
    :param path: path
    :param header: optional for json
    :param data:
    :return:
    """
    if path.endswith('.json'):
        return load_data_from_json(path)
    if path.endswith('.csv'):
        return load_data_from_csv(path)
    if path.endswith('.xlsx'):
        return load_data_from_xlsx(path)
    return []


def uniform_write(path: str, data, header=None):
    if path.endswith('.json'):
        write_json_to_file(path, data)
        return
    if path.endswith('.csv'):
        if not header:
            header = data[0].keys()
        write_csv_to_file(path, header, data)


if __name__ == '__main__':
    _, z = uniform_read(path='tmp/dv_input/client/Muse_2019.08_post_back_attribution.xlsx')
    print(z[:5])
    uniform_write('tmp/dv_output/output.json', z)
    header, z = uniform_read(path='tmp/dv_input/dv/report.201909.kissmyads_int.csv')
    print(z[:5])
    uniform_write('tmp/dv_output/output.csv', z, header)
