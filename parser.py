from sys import argv
from py_pdf_parser.loaders import load_file
from py_pdf_parser import tables
import csv
from tabulate import tabulate
import re

docname = argv[1] if len(argv) > 1 else './fichas/ES-00981.pdf'
out_docname = argv[2] if len(argv) > 2 else 'parser.csv'

FONT_MAPPING = {
  "Helvetica-Bold,12.0": "header",
  "Helvetica,9.0": "table_element",
  "Helvetica-Bold,9.0": "footer_end",
  "Helvetica-Bold,10.0": "header_start",
}
document = load_file(docname, font_mapping=FONT_MAPPING)

headers = document.elements.filter_by_font("header")

header = headers.filter_by_text_equal(
  "Usos y Dosis Autorizados"
).extract_single_element()

post_table = headers.filter_by_text_contains(
  "Plazos de Seguridad (Protección del Consumidor)"
).extract_single_element()

elements = document.elements.between(
  header, post_table
# ).filter_by_regex(
#   "^[^P][^á][^g][^i][^n][^a]"
# ).filter_by_regex(
#   "[^0-9]"
# ).filter_by_regex(
#   "^[^D][^e][^\\s][^0-9]+$"
).filter_by_font("table_element")

table = tables.extract_table(
  elements,
  as_text=True,
  fix_element_in_multiple_rows=True,
  fix_element_in_multiple_cols=True,
)

def thead():
  return table[0]

def column(n = 0):
  arr = []
  for row in table:
    arr.append(row[n])

  return arr

def to_csv(filename = out_docname, table = table):
  with open(filename, 'w') as f:
    file = csv.writer(f)
    file.writerows(table)

def single_page_format():
  arr = []
  for row in table:
    arr.append([row[0], row[1], row[2]])

  return arr

# Actualmente 'single_page_format' sirve para todas las tablas.
# Con el nuevo formato directamente no funciona
def multi_page_format():
  arr = []
  for row in table:
    por_filtrar = row[6]

    if (re.search('^Ámbito', por_filtrar)):
      por_filtrar = ''

    usos = row[0] + row[1] + row[2]
    agentes = row[3]
    dosis = por_filtrar + row[7]

    if (re.search('Página', usos)):
      usos = ''
    arr.append([usos, agentes, dosis])

  multi_page_fix(arr)
  return arr

def multi_page_fix(table):
  arr = []
  for i in range(0, len(table)):
    row = table[i]
    if not row[1]:
      last_row = table[i-1]
      print('---MATCH----')
      print('---BEFORE---')
      print(last_row)
      print('---ROW------')
      print(row)

  return arr

def format():
  # if thead()[0] == '':
  #   return multi_page_format()
  return single_page_format()

# formated_table = format()
# to_csv(table=formated_table)
# print(tabulate(formated_table))

print(to_csv())
