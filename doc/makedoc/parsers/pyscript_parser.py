from .concept import FileParserAbstract

class PyscriptParser(FileParserAbstract):

    def __init__(self, **kwargs):
        super(PyscriptParser, self).__init__(**kwargs)

    def get_parsed_doc(self) -> str:
        if self.parsed_doc == '':
            self.parsed_doc = f'# {self.name}\n'
        return self.parsed_doc
