from sys import argv
import py_pdf_parser as parser
from py_pdf_parser import loaders
from py_pdf_parser.visualise import visualise

docname = argv[1] if len(argv) > 1 else './fichas/ES-00981.pdf'
document = loaders.load_file(docname)

visualise(document, show_info=True)
