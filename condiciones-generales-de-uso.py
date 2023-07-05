from parser import UsageConditionsParser, UsageConditionsParserCollection
import argparse

# Argumentos
parser = argparse.ArgumentParser(description="Parser para PDFs de productos fitosanitarios")
parser.add_argument('pdf_name', type=str, help='Archivo PDF del que sacar la información')
args = parser.parse_args()

print(UsageConditionsParserCollection([
  UsageConditionsParser(args.pdf_name),
  UsageConditionsParser('./pdf_vademecum/ENERO 2023/11420.pdf')
]).to_dictionary_list())
