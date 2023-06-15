from parser import Parser, ParserDiff
from sys import argv
from tabulate import tabulate
from rich import print as rprint

def printDiffs(diffs: list[ParserDiff]):
    dictionaryDiffs = []
    for diff in diffs:
        dictionaryDiffs.append(diff.__dict__)

    rprint(dictionaryDiffs)

docname = argv[1] if len(argv) > 1 else './fichas/ES-00318.pdf'
out_docname = argv[2] if len(argv) > 2 else 'parser.csv'

diffs: list[ParserDiff] = []

parser = Parser(docname, out_docname)
parser2 = Parser('./fichas/ES-00361.pdf', out_docname)

diffs += parser.diff(parser2)

printDiffs(diffs)

