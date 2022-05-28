from abc import ABC, abstractmethod
from typing import Union, List
import pathlib
import re

class ParserAbstract(ABC):

    VERSION = '1.2.0'

    class Paths:

        makedoc = pathlib.Path(__file__).resolve().parents[2].absolute()

        doc = makedoc.parent
        src = doc.parent

        logs = makedoc/'logs'
        config = makedoc/'config'
        packed_doc = makedoc/"packed_doc"

        ignored_path = config/'makedoc.ignored_path'
        ignored_every = config/'makedoc.ignore_every'
        ignored_extensions = config/'makedoc.ignored_extensions'


    def __init__(
            self,
            path:pathlib.Path,
            root_path:Union[None, pathlib.Path]=None
    ):
        self.path = path
        self.root_path = root_path
        self.name = str(self.path).split('/')[-1]
        self.parsed_doc:str = ''

        if self.root_path is None:
            self.root_path = self.Paths.src

    @abstractmethod
    def get_parsed_doc(self) -> str:
        if self.parsed_doc == '':
            self.parsed_doc = ''
        return self.parsed_doc

    @abstractmethod
    def get_hierarchy_repr(self) -> str:
        return ''

    def is_ignored(self) -> bool:
        with open(self.Paths.ignored_path, 'r') as f:
            lines = f.readlines()
        for l in lines:
            if l[0] != '#' and \
                    l.strip() == str(self.path) or \
                    l.strip() == self.get_partial_path() or \
                    (l.strip() == '/'.join(self.get_partial_path().split('/')[:-1]) + '/' and l.strip()!=''):
                return True
        with open(self.Paths.ignored_every, 'r') as f:
            lines = f.readlines()
        for l in lines:
            if l[0] != '#' and l.strip() == self.name:
                return True
        if self.path.is_file():
            with open(self.Paths.ignored_extensions, 'r') as f:
                lines = f.readlines()
            for l in lines:
                if l[0] != '#' and l.strip() == '.'.join(self.name.split('.')[1:]):
                    return True
        return False

    def get_partial_path(self):
        fullpath = str(self.path.absolute())
        root_path = str(self.root_path.absolute())
        return fullpath[len(root_path)+1:]

    def __repr__(self):
        return str(self.get_partial_path())