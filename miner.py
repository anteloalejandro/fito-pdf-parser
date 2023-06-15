from sys import argv
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine
from pdfminer.layout import LTChar

docname = argv[1] if len(argv) > 1 else './fichas/ES-00981.pdf'

doc_pages = [*extract_pages(docname)]
for element in doc_pages[2]:
  if isinstance(element, LTTextContainer):
    for line in element:
      if isinstance(line, LTTextLine):
        print(line.get_text())
        print('--')

# for page in extract_pages(docname):
#   for element in page:
#     if isinstance(element, LTTextContainer):
#       print(element.get_text())
