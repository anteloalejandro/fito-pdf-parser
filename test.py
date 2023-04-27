import py_pdf_parser as parser
from py_pdf_parser import loaders
from py_pdf_parser.visualise import visualise

document = loaders.load_file('./fichas/ES-00981.pdf')

visualise(document, show_info=True)
