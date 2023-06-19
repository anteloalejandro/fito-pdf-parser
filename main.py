import hashlib
from parser import Parser, ParserDiffCollection
from colorama import Fore
from os import listdir
from os.path import isdir, isfile, join
from rich import print as rprint
from json import dumps as json
import argparse

# Argumentos
parser = argparse.ArgumentParser(description="Parser para PDFs de productos fitosanitarios")
parser.add_argument('-o', '--out', type=str, help='Archivo JSON de salida')
parser.add_argument('--old', type=str, help='Directorio con las versiones viejas de los PDF')
parser.add_argument('--new', type=str, help='Directorio con las versiones nuevas de los PDF')
parser.add_argument('-s', '--silent', action='store_true', help='Directorio con las versiones nuevas de los PDF')
args = parser.parse_args()

def warning(msg: str):
  msg = 'Aviso: %s' % msg
  if args.silent:
    log('warnings.log', msg)
  else:
    print(Fore.LIGHTYELLOW_EX + msg + Fore.RESET)

def error(msg: str):
  msg = 'Error: %s' % msg
  if args.silent:
    log('errors.log', msg)
  else:
    print(Fore.LIGHTRED_EX + msg + Fore.RESET)

def log(file: str, msg: str):
  f = open(file, 'a')
  f.write('%s\n' % msg)
  f.close()

def printDiffs(diffs: ParserDiffCollection):
  rprint(diffs.to_grouped_dictionary_list())

def writeDiffs(diffs: ParserDiffCollection, to: str):
  file = open(to, "w")
  jsonDiffs = json(diffs.to_grouped_dictionary_list(), indent=4, ensure_ascii=False)

  file.writelines(jsonDiffs.splitlines(True))

  file.close()

def get_files(path: str) -> list[str]:
  if isfile(path):
    error('%s no es un directorio' % path)
    return []
  files: list[str] = []
  for f in listdir(path):
    file = join(path, f)
    if isfile(file): files.append(file)

  return files

def hash_file(file: str) -> str:
  hash = hashlib.md5()
  with open(file, 'rb') as f:
    chunk = 0
    while chunk != b'':
      chunk = f.read(1024)
      hash.update(chunk)

  return hash.hexdigest()

# Rutas
old_path = './old' if args.old == None else args.old
new_path = './new' if args.new == None else args.new
old_files = get_files(old_path)
new_files = get_files(new_path)

# Sacar diferencias entre PDFs
diffs = ParserDiffCollection()

for old_file in old_files:
  new_file_path = old_file.replace(old_path, new_path)
  try:
    new_file_idx = new_files.index(new_file_path)
  except ValueError as e:
    warning('%s no ha sido actualizado' % old_file)
    continue

  new_file = new_files[new_file_idx]

  # Si son idénticos, no parsear
  # if (hash_file(old_file) == hash_file(new_file)):
  #   continue

  current_file = ''
  try:
    current_file = old_file
    old_parser = Parser(current_file)
    current_file = new_file
    new_parser = Parser(current_file)
    diffs.add(new_parser.diff(old_parser))
  except Exception as e:
    error('%s ON %s' % (e.__str__(), current_file))


## DEBUG
# print('<============  %s  =============>' % old_file)
# print(tabulate(old_parser.format()))
# print('<============  %s  =============>' % new_file)
# print(tabulate(new_parser.format()))



# Mostrar resultado
printDiffs(diffs)

# Exportar resultado (JSON)
if args.out != None:
  if isdir(args.out):
    error('%s es un directorio' % args.out)
  else:
    writeDiffs(diffs, args.out)
