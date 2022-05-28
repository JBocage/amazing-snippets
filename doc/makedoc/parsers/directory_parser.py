import os
import datetime

from .concept import ParserAbstract
from .concept import FileParserAbstract
from .pyscript_parser import PyscriptParser
from typing import List

class DirectoryParser(ParserAbstract):

    EXTENSION_MATCHING = {
        'py':PyscriptParser
    }

    def __init__(self, **kwargs):
        super(DirectoryParser, self).__init__(**kwargs)

        self.packed_doc_loc = self.Paths.packed_doc / self.get_partial_path()
        self.packed_doc_filename = f'{self.name}.md'
        self.packed_doc_path = self.packed_doc_loc/self.packed_doc_filename
        self.dir_children:List[DirectoryParser]=[]
        self.file_children:List[FileParserAbstract]=[]
        if not self.is_ignored():
            self._init_packed_doc()
            self._mine_for_doc()

    def _init_packed_doc(self):
        self.packed_doc_loc.mkdir(exist_ok=True)
        if not self.packed_doc_path.exists():
            with open(self.packed_doc_path, 'w+') as f:
                f.write(f"# {self.name}\n")

    def _mine_for_doc(self):
        self.dir_children: List[DirectoryParser] = []
        self.file_children: List[FileParserAbstract] = []
        for fname in os.listdir(self.path):
            if (self.path/fname).is_dir():
                child = DirectoryParser(path=self.path/fname, root_path=self.root_path)
                if not child.is_ignored():
                    self.dir_children.append(child)
            else:
                if fname.split('.')[-1] in self.EXTENSION_MATCHING.keys():
                    child = self.EXTENSION_MATCHING[fname.split('.')[-1]](path=self.path / fname, root_path=self.root_path)
                else:
                    child = FileParserAbstract(path=self.path/fname, root_path=self.root_path)
                if not child.is_ignored():
                    self.file_children.append(child)
        self.dir_children.sort(key=lambda x:x.name)
        self.file_children.sort(key=lambda x:x.name)

    def get_parsed_doc(self) -> str:
        if self.parsed_doc == '':
            with open(self.packed_doc_path, 'r') as f:
                self.parsed_doc = ''.join(f.readlines())
        return self.parsed_doc

    def get_doc_file_content(self) -> str:
        content = ''

        content += self.get_parsed_doc()

        content += f'\n' \
                   f'<hr style="border:2px solid gray"> </hr>\n' \
                   f'\n' \
                   f'# Structure\n' \
                   f'\n' \
                   f'```\n'
        content += self.get_hierarchy_repr()
        content += f'\n```\n' \
                   f'<hr style="border:2px solid gray"> </hr>\n' \
                   f'\n'

        for subdir in self.dir_children:
            subdirdoc = subdir.get_parsed_doc()
            for line in subdirdoc.split('\n'):
                if line[:1] == '#':
                    content += f'#{line}\n'
                else:
                    content += f'>{line}\n'
            content += '\n' \
                       '---\n' \
                       '\n'

        content += f'\n\n\n\n<sub>This doc was automatically generated with makedoc v{self.VERSION} on {datetime.datetime.now().strftime(" %D %H:%M:%S ")}'
        return content

    def get_hierarchy_repr(self) -> str:
        FCROSS = '└── '
        CROSSDIR = '├── '
        VERTLINE = '│   '
        NOTHING = '    '
        output = self.name + '/\n'
        n_childs = len(self.dir_children) + len(self.file_children)
        i=0
        for subdir in self.dir_children:
            i += 1
            subdir_hierarchy = subdir.get_hierarchy_repr()
            marker = CROSSDIR if i != n_childs else FCROSS
            for line in subdir_hierarchy.split('\n'):
                output += marker + line + '\n'
                marker = VERTLINE if i != n_childs else NOTHING
        for subfile in self.file_children:
            i += 1
            marker = CROSSDIR if i != n_childs else FCROSS
            output += marker + subfile.get_hierarchy_repr() + '\n'
        return output[:-1]

    def parse_doc(self) -> str:
        pass