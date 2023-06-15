from parser import Parser, ParserDiff
from sys import argv
from tabulate import tabulate
from os import listdir
from os.path import isfile, join
from rich import print as rprint
from json import dumps as json

def diffsToDicts(diffs: list[ParserDiff]):
  dictionaryDiffs: list[dict] = []
  for diff in diffs:
    dictionaryDiffs.append(diff.__dict__)

  return dictionaryDiffs;

def printDiffs(diffs: list[ParserDiff]):
  rprint(diffsToDicts(diffs))

def writeDiffs(diffs: list[ParserDiff], to: str):
  file = open(to, "w")
  jsonDiffs = json(diffsToDicts(diffs), indent=4, ensure_ascii=False)

  file.writelines(jsonDiffs.splitlines(True))

  file.close()

def get_files(path: str) -> list[str]:
  files: list[str] = []
  for f in listdir(path):
    file = join(path, f)
    if isfile(file): files.append(file)

  return files

docname = argv[1] if len(argv) > 1 else './fichas/ES-00318.pdf'
out_docname = argv[2] if len(argv) > 2 else 'parser.csv'

old_path = './old'
new_path = './new'
old_files = get_files(old_path)
new_files = get_files(new_path)

diffs: list[ParserDiff] = []

for old_file in old_files:
  new_file_path = old_file.replace(old_path, new_path)
  try:
    new_file_idx = new_files.index(new_file_path)
  except ValueError as e:
    print('Aviso: %s no ha sido actualizado' % old_file)
    continue


  new_file = new_files[new_file_idx]

  old_parser = Parser(old_file)
  new_parser = Parser(new_file)

  ## DEBUG
  # print('<============  %s  =============>' % old_file)
  # print(tabulate(old_parser.format()))
  # print('<============  %s  =============>' % new_file)
  # print(tabulate(new_parser.format()))

  diffs += new_parser.diff(old_parser)

printDiffs(diffs)

