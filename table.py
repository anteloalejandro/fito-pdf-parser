from sys import argv
import camelot
from tabulate import tabulate

docname = argv[1] if len(argv) > 1 else './fichas/ES-00981.pdf'


tables = camelot.read_pdf(docname, pages="all")

tables.export("output.csv", f="csv")

print(tables)
