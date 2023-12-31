from os import replace
import re
from typing import Any
from matplotlib import text
from unidecode import unidecode
from py_pdf_parser.loaders import load_file
from py_pdf_parser import tables
import csv
import itertools

class TableParserDiff:
  def __init__(self, docname: str, msg: str, parserText = '', otherParserText = ''):
    self.docname = docname
    self.msg = msg
    self.diff = None if parserText == '' or otherParserText == '' else {
      'from': otherParserText,
      'to': parserText
    }

    self.__dict__ = {
      "docname": self.docname,
      "msg": self.msg,
      "diff": self.diff
    }

  def __str__(self) -> str:
    return str(self.__dict__)

  def __unicode__(self) -> str:
    return self.__str__()

  def __repr__(self) -> str:
    return self.__str__()

class TableParserDiffCollection:
  diffs: list[TableParserDiff]

  def __init__(self, diffs: list[TableParserDiff] | None = None):
    self.diffs = diffs if diffs != None else []

  def add(self, other: 'TableParserDiffCollection'):
    self.diffs += other.diffs

  def append(self, other: 'TableParserDiff'):
    self.diffs.append(other);

  def to_dictionary_list(self):
    dictionary_diffs: list[dict] = []
    for diff in self.diffs:
      dictionary_diffs.append(diff.__dict__)

    return dictionary_diffs;

  def to_grouped_dictionary_list(self):
    grouped: list[dict] = []
    for key, values in itertools.groupby(self.diffs, key=lambda x:x.docname):
      grouped += [{
        'docname': key,
        'changes': [{
          "msg": diff.msg,
          "diff": diff.diff
        } for diff in values]
      }]

    return grouped

class TableParser:

  def __init__(self, pdf_name: str, csv_name: str | None = None):
    self.docname = pdf_name
    self.out_docname = csv_name if csv_name != None else pdf_name.replace('.pdf', '.csv')

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

    self.elements = self.document.elements.between(
      self.header, self.post_table
    ).filter_by_font("table_element")

    self.table = tables.extract_table(
      self.elements,
      as_text=True,
      fix_element_in_multiple_rows=True,
      fix_element_in_multiple_cols=True,
    )

  def to_csv(self, filename = None, table = None):
    if filename == None: filename = self.out_docname
    if table == None: table = self.format()

    with open(filename, 'w') as f:
      file = csv.writer(f)
      file.writerows(table)

  def format(self):
    arr = []
    for row in self.table:
      n_of_columns = min(3, len(row))
      arr.append([
        row[cell_idx]
        for cell_idx in range(0, n_of_columns)
      ])

    return arr

  def get_raw_text(self):
    arr = []
    for e in self.elements:
      arr.append(e.text())

    return arr

  def equals(self, other: 'TableParser'):
    return ''.join(self.get_raw_text()) == ''.join(other.get_raw_text());

  def diff(self, other: 'TableParser') -> TableParserDiffCollection:
    collection = TableParserDiffCollection()
    selfLen = len(self.table)
    otherLen = len(other.table)
    if selfLen != otherLen:
      collection.append(TableParserDiff(self.docname, 'La cantidad de elementos no coincide'))
      # Evitar reporte de errores inexacto cuando la cantidad de elementos no coincide
      return collection

    for index in range(0, min(selfLen, otherLen)):
      n_of_columns = min(3, len(self.table[0]), len(other.table[0]))

      selfText = unidecode(
        '; '.join([
          self.table[index][cell_idx]
          for cell_idx in range(0, n_of_columns)
        ]).lower()
      )
      otherText = unidecode(
        '; '.join([
          other.table[index][cell_idx]
          for cell_idx in range(0, n_of_columns)
        ]).lower()

      )

      if (selfText != otherText):
        collection.append(TableParserDiff(self.docname, 'El texto no coincide', selfText, otherText))


    return collection

class UsageConditionsParser:
  def __init__(self, pdf_name: str, csv_name: str | None = None):
    self.docname = pdf_name
    self.out_docname = csv_name if csv_name != None else pdf_name.replace('.pdf', '.csv')

    self.FONT_MAPPING = {
      "Helvetica-Bold,12.0": "header",
      "Helvetica,11.0": "text",
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

    filtered_headers = self.headers.filter_by_text_equal(
      "Condiciones Generales de Uso"
    )
    self.header = None
    if (len(filtered_headers) > 0):
      self.header = filtered_headers.extract_single_element()

    self.post_text = self.headers.filter_by_text_contains(
      "Clase de Usuario"
    ).extract_single_element()

    if (self.header != None):
      self.elements = self.document.elements.between(
        self.header, self.post_text
      ).filter_by_font("text")
    else:
      self.elements = self.document.elements.filter_by_text_contains("Condiciones Generales de Uso").before(self.post_text)

    self.__dict__ = {
      "docname": self.docname,
      "text": self.__str__()
    }

  def __str__(self) -> str:
    out = ''
    for e in self.elements:
      text = e.text()

      if self.header == None:
        # text = text.replace("Condiciones Generales de Uso", '')
        text = re.sub('^Condiciones Generales de Uso', '', text)

      out += text + ' '

    return out

class UsageConditionsParserCollection:
  usage_conditions: list[UsageConditionsParser]

  def __init__(self, usage_conditions: list[UsageConditionsParser] | None = None):
    self.usage_conditions = usage_conditions if usage_conditions != None else []

  def add(self, other: 'UsageConditionsParserCollection'):
    self.usage_conditions += other.usage_conditions

  def append(self, other: 'UsageConditionsParser'):
    self.usage_conditions.append(other);

  def to_dictionary_list(self):
    dictionary: list[dict] = []
    for uc in self.usage_conditions:
      dictionary.append(uc.__dict__)

    return dictionary;
