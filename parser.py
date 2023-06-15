from sys import argv
from py_pdf_parser.loaders import load_file
from py_pdf_parser import tables
import csv
from tabulate import tabulate
import re
from py_pdf_parser.visualise import visualise

class Parser:

  def __init__(self, pdf_name, csv_name):
    self.docname = pdf_name
    self.out_docname = csv_name

    self.FONT_MAPPING = {
      "Helvetica-Bold,12.0": "header",
      "Helvetica,9.0": "table_element",
      "Helvetica-Bold,9.0": "heading_start",
      "Helvetica-Bold,10.0": "footer_end",
    }
    self.document = load_file(self.docname, font_mapping=self.FONT_MAPPING)

    self.headers = self.document.elements.filter_by_font("header")

    self.headings = self.document.elements.filter_by_font("heading_start").filter_by_text_equal(
      "DIRECCIÓN GENERAL DE SANIDAD DE\nLA PRODUCCIÓN AGRARIA"
    )

    self.footers = self.document.elements.filter_by_font("footer_end").filter_by_text_equal(
      "Página"
    )

    self.header = self.headers.filter_by_text_equal(
      "Usos y Dosis Autorizados"
    ).extract_single_element()

    self.post_table = self.headers.filter_by_text_contains(
      "Plazos de Seguridad (Protección del Consumidor)"
    ).extract_single_element()

    page = 2
    heading = self.headings[page]
    footer = self.footers[page]
    self.elements = self.document.elements.after(self.header).before(self.post_table).between(
      heading, footer
    ).filter_by_font("table_element")

    page += 1
    while (page < len(self.headings)):
      heading = self.headings[page]
      footer = self.footers[page]
      elements = self.document.elements.after(self.header).before(self.post_table).between(
        heading, footer
      ).filter_by_font("table_element")
      self.elements = self.elements.add_elements(
        *elements
      )
      page += 1

    self.table = tables.extract_table(
      self.elements,
      as_text=True,
      fix_element_in_multiple_rows=True,
      fix_element_in_multiple_cols=True,
      tolerance=1000
    )

  def thead(self):
    return self.table[0]

  def column(self, n = 0):
    arr = []
    for row in self.table:
      arr.append(row[n])

    return arr

  def to_csv(self, filename = None, table = None):
    if filename == None: filename = self.out_docname
    if table == None: table = self.table

    with open(filename, 'w') as f:
      file = csv.writer(f)
      file.writerows(table)

  def single_page_format(self):
    arr = []
    for row in self.table:
      arr.append([row[0], row[1], row[2]])

    return arr

# Actualmente 'single_page_format' sirve para todas las tablas.
# Con el nuevo formato directamente no funciona
  def multi_page_format(self):
    arr = []
    for row in self.table:
      por_filtrar = row[6]

      if (re.search('^Ámbito', por_filtrar)):
        por_filtrar = ''

      usos = row[0] + row[1] + row[2]
      agentes = row[3]
      dosis = por_filtrar + row[7]

      if (re.search('Página', usos)):
        usos = ''
      arr.append([usos, agentes, dosis])

    self.multi_page_fix(arr)
    return arr

  def multi_page_fix(self, table):
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

  def format(self):
    # if thead()[0] == '':
    #   return multi_page_format()
    return self.single_page_format()

  def get_raw_text(self):
    arr = []
    for e in self.elements:
      arr.append(e.text())
    return arr

  def list_elements(self):
    element_list = self.get_raw_text()
    for i in range(0, len(element_list)):
      print(i+1, element_list[i], '\n')

# formated_table = format()
# to_csv(table=formated_table)
# print(tabulate(formated_table))

# print(to_csv())

docname = argv[1] if len(argv) > 1 else './fichas/ES-00318.pdf'
out_docname = argv[2] if len(argv) > 2 else 'parser.csv'

parser = Parser(docname, out_docname)

print(tabulate(parser.format()))
