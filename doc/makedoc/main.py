import pathlib
import sys


class Paths:
    makedoc = pathlib.Path(__file__).resolve().absolute()
    doc = makedoc.parent
    src = doc.parent

if not str(Paths.makedoc) in sys.path:
    sys.path.append(str(Paths.makedoc))

from parsers.source_directory_parser import SourceDirectoryParser


if __name__ == '__main__':
    dp = SourceDirectoryParser(
        path=SourceDirectoryParser.Paths.doc.parent,
    )
    print(dp.get_hierarchy_repr())
    dp.save_readme()
