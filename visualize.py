from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise

doc = load_file('./pdf_vademecum/ENERO 2023/11179.pdf')

visualise(doc, show_info=True)
