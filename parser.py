from typing import Any
from py_pdf_parser.loaders import load_file
from py_pdf_parser import tables
import csv
import itertools

class ParserDiff:
  def __init__(self, docname: str, msg: str, parserText = '', otherParserText = ''):
    self.docname = docname
    self.msg = msg
    self.diff = None if parserText == '' or otherParserText == '' else {
      'to': parserText,
      'from': otherParserText
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

class ParserDiffCollection:
  diffs: list[ParserDiff]

  def __init__(self, diffs: list[ParserDiff] | None = None):
    self.diffs = diffs if diffs != None else []

  def add(self, other: 'ParserDiffCollection'):
    self.diffs += other.diffs

  def append(self, other: 'ParserDiff'):
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

class Parser:

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

  def format(self):
    arr = []
    for row in self.table:
      arr.append([row[0], row[1], row[2]])

    return arr

  def get_raw_text(self):
    arr = []
    for e in self.elements:
      arr.append(e.text())
    return arr

  def list_elements(self):
    element_list = self.get_raw_text()
    for i in range(0, len(element_list)):
      print(i+1, element_list[i], '\n')

  def equals(self, other: 'Parser'):
    return ''.join(self.get_raw_text()) == ''.join(other.get_raw_text());

  def diff(self, other: 'Parser') -> ParserDiffCollection:
    collection = ParserDiffCollection()
    selfLen = len(self.table)
    otherLen = len(other.table)
    if selfLen != otherLen:
      collection.append(ParserDiff(self.docname, 'La cantidad de elementos no coincide'))

    for index in range(0, min(selfLen, otherLen)):
      selfText = ''.join(self.table[index])
      otherText = ''.join(other.table[index])
      if (selfText != otherText):
        collection.append(ParserDiff(self.docname, 'El texto no coincide', selfText, otherText))


    return collection
