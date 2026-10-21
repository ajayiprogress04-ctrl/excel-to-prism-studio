"""Convert Excel worksheets to GraphPad Prism PZFX data tables.

Requires Python 3.9+ and: py -m pip install pandas openpyxl xlrd
Examples:
  py excel_to_prism.py experiment.xlsx --type column
  py excel_to_prism.py experiment.xlsx --type xy -o results.pzfx
  py excel_to_prism.py experiment.xlsx --sheet Sheet1 --type xy

First row: column titles. Remaining rows: numbers or blanks.
Column mode: each column is a group of individual observations.
XY mode: first column is X; remaining columns are individual Y datasets.
Does not create graphs, analyses, grouped tables, or replicate subcolumns.
Excel formulas require saved calculated values. Not tested inside Prism 10.
"""
import argparse
import math
import re
from datetime import time, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd


def excel_column_name(index):
    label = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label


def numeric_text(value, sheet, row, column):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
    if isinstance(value, bool):
        raise ValueError(f"Sheet '{sheet}', cell {column}{row}: Boolean values are unsupported.")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Sheet '{sheet}', cell {column}{row}: Expected a number, found {value!r}.") from None
    if not math.isfinite(number):
        raise ValueError(f"Sheet '{sheet}', cell {column}{row}: Infinite values are unsupported.")
    return format(number, '.17g')


def duration_seconds(value):
    """Parse unambiguous h:mm:ss[.fraction] durations; never infer Excel serial units."""
    if isinstance(value, timedelta):
        return value.total_seconds()
    if isinstance(value, time):
        return value.hour * 3600 + value.minute * 60 + value.second + value.microsecond / 1e6
    if isinstance(value, str):
        match = re.fullmatch(r"(\d+):([0-5]\d):([0-5]\d(?:\.\d+)?)", value.strip())
        if match:
            h, m, sec = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(sec)
    raise ValueError(f"Expected duration h:mm:ss[.fraction], found {value!r}.")


def prepare_column(values, title, sheet, column, time_unit):
    present = [v for v in values if not pd.isna(v) and not (isinstance(v, str) and not v.strip())]
    time_like = any(isinstance(v, (time, timedelta)) or (isinstance(v, str) and ':' in v) for v in present)
    if time_unit != 'none' and time_like:
        converted = []
        for r, value in enumerate(values, 2):
            if pd.isna(value) or (isinstance(value, str) and not value.strip()):
                converted.append(None)
                continue
            try:
                number = duration_seconds(value) / (60 if time_unit == 'minutes' else 1)
            except ValueError as error:
                raise ValueError(f"Sheet '{sheet}', cell {column}{r}: {error}") from None
            converted.append(format(number, '.17g'))
        return f'{title} ({time_unit})', converted
    return title, [numeric_text(v, sheet, r, column) for r, v in enumerate(values, 2)]


def add_data_column(table, tag, title, values):
    column = ET.SubElement(table, tag, Width='100', Decimals='6', Subcolumns='1')
    ET.SubElement(column, 'Title').text = str(title)
    subcolumn = ET.SubElement(column, 'Subcolumn')
    for value in values:
        cell = ET.SubElement(subcolumn, 'd')
        if value is not None:
            cell.text = value


def convert_excel_to_prism(input_file, output_file=None, table_type='column', sheet_name=None, time_unit='none'):
    input_path = Path(input_file).expanduser().resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f'Excel file not found: {input_path}')
    if input_path.suffix.lower() not in {'.xlsx', '.xlsm', '.xls'}:
        raise ValueError('Use an .xlsx, .xlsm, or .xls file.')
    if table_type not in {'column', 'xy'}:
        raise ValueError("Table type must be 'column' or 'xy'.")
    output_path = Path(output_file).expanduser().resolve() if output_file else input_path.with_suffix('.pzfx')
    if output_path.suffix.lower() != '.pzfx':
        raise ValueError('Output filename must end with .pzfx.')
    if output_path.exists():
        raise FileExistsError(f'Output already exists: {output_path}. Choose another filename.')

    if time_unit not in {'none', 'seconds', 'minutes'}:
        raise ValueError('Time unit must be none, seconds or minutes.')
    tables = []
    with pd.ExcelFile(input_path) as workbook:
        selected = [sheet_name] if sheet_name is not None else workbook.sheet_names
        for name in selected:
            if name not in workbook.sheet_names:
                raise ValueError(f'Worksheet not found: {name}')
            raw = pd.read_excel(workbook, sheet_name=name, header=None, dtype=object)
            while len(raw) and raw.iloc[-1].isna().all():
                raw = raw.iloc[:-1]
            while raw.shape[1] and raw.iloc[:, -1].isna().all():
                raw = raw.iloc[:, :-1]
            if raw.empty or len(raw) < 2:
                continue
            titles = [str(v).strip() if pd.notna(v) and str(v).strip() else f'Column {i + 1}'
                      for i, v in enumerate(raw.iloc[0])]
            data = raw.iloc[1:].reset_index(drop=True)
            if table_type == 'xy' and data.shape[1] < 2:
                raise ValueError(f"Sheet '{name}' needs X and at least one Y column.")
            prepared = [prepare_column(list(data.iloc[:, c]), titles[c], name,
                                       excel_column_name(c), time_unit)
                        for c in range(data.shape[1])]
            titles = [item[0] for item in prepared]
            columns = [item[1] for item in prepared]
            tables.append((name, titles, columns))
    if not tables:
        raise ValueError('No worksheets containing data were found.')

    root = ET.Element('GraphPadPrismFile', PrismXMLVersion='5.00')
    sequence = ET.SubElement(root, 'TableSequence')
    for i in range(len(tables)):
        ET.SubElement(sequence, 'Ref', ID=f'Table{i}', Selected='1')
    for i, (name, titles, columns) in enumerate(tables):
        first_y = 1 if table_type == 'xy' else 0
        tag = 'HugeTable' if len(columns) - first_y > 104 else 'Table'
        table = ET.SubElement(root, tag, {
            'ID': f'Table{i}', 'XFormat': 'numbers' if first_y else 'none',
            'YFormat': 'replicates', 'Replicates': '1',
            'TableType': 'XY' if first_y else 'OneWay',
            'EVFormat': 'AsteriskAfterNumber',
        })
        ET.SubElement(table, 'Title').text = name
        if first_y:
            add_data_column(table, 'XColumn', titles[0], columns[0])
        for c in range(first_y, len(columns)):
            add_data_column(table, 'YColumn', titles[c], columns[c])
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('xb') as destination:
        tree.write(destination, encoding='utf-8', xml_declaration=True)
    print(f'Created: {output_path}')
    print(f'Converted {len(tables)} worksheet(s).')
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Convert Excel worksheets to Prism PZFX data tables.')
    parser.add_argument('input', help='Input Excel workbook')
    parser.add_argument('-o', '--output', help='Output .pzfx filename')
    parser.add_argument('--type', choices=['column', 'xy'], default='column', help='Default: column')
    parser.add_argument('--sheet', help='Worksheet name; default: all worksheets')
    parser.add_argument('--time-unit', choices=['none', 'seconds', 'minutes'], default='none',
                        help='Explicit conversion of duration columns; numeric columns are unchanged')
    args = parser.parse_args()
    try:
        convert_excel_to_prism(args.input, args.output, args.type, args.sheet, args.time_unit)
    except Exception as error:
        parser.exit(1, f'Conversion failed: {error}\n')


if __name__ == '__main__':
    main()
