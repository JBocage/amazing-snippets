from .parser_abstract import ParserAbstract
from typing import List

class FileParserAbstract(ParserAbstract):

    def __init__(self, **kwargs):
        super(FileParserAbstract, self).__init__(**kwargs)

    def get_hierarchy_repr(self) -> str:
        return self.name

    def get_parsed_doc(self) -> str:
        return ''

    def readlines_as_txt(self) -> List[str]:
        with open(self.path, 'r') as f:
            lines = f.readlines()
        return lines