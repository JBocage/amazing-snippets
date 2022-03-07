"""
> author: JBocage

This script automatically generates the documentation skeleton for the project.

It aims to function from every source directory. It is easy to use it. An sample of what is contained in the file is given here.

```python

root_path = pathlib.Path(os.path.abspath(os.path.join(__file__,'..',)))     # initialise the source path

source_parser = DocParser(root_path,                                        # create the parser
               ignored_dirs=['venv',
                             '.git',
                             '.idea',
                             ],
               )
source_parser.makedoc(update_README=True,                                   # generate the doc
                      )

recursive_parser = DocParser(root_path.joinpath('src',),                    # another example of parser
                            )
recursive_parser.makedoc(recurse=True,                                      # another example of doc generation call
                         verbose=False)
```
"""

import pathlib
import os
import re
import time
import datetime
import numpy as np

root_path = pathlib.Path(os.path.abspath(os.path.join(__file__,
                                                      '..',
                                                      )))

class DocParser():
    DIRDOCNAME = 'dir_doc.md'
    PARSABLE_FILES = {
        r'\.py' : "python",
        r'\.md' : "markdown"
    }
    OUTPUTFILE = 'AUTODOC.md'
    IGNORED_MD_FILES = [
        'README.md'
    ]
    IGNORED_DIRS = ['__pycache__',
                    '.makedoc']
    MAX_DIR_SIZE = 20 # files
    IGNORE_MARKER = 'autodoc.ignore'

    VERSION = '1.1.0'

    MAKEDOC_DIR_PATH = pathlib.Path(os.path.abspath(os.path.join(__file__,
                                                            '../.makedoc')))
    IGNORED_DIRS_FILENAME = 'ignored.mkdc'

    def __init__(self,
                 path:pathlib.Path,
                 ignored_dirs=[],
                 ):
        self._init_makedoc_dir()

        self.name = path.name
        self.is_dir = path.is_dir()
        self.is_file = path.is_file()
        self.path = path.absolute()
        self.ignored = False
        self.ignore_in_doc = False
        self.ignore_in_struct = False

        self.ignored_dirs = ignored_dirs + self.IGNORED_DIRS
        self._update_ignored_dirs()

        self.children = []

        self.docstrings = []
        self.md_strings = []

        self.process_warnings = []

        self._parse_doc()
        self._dig_for_docs(maxdepth=3)

        self.type = None

    def _init_makedoc_dir(self):
        self.MAKEDOC_DIR_PATH.mkdir(exist_ok=True)
        if not self.IGNORED_DIRS_FILENAME in os.listdir(self.MAKEDOC_DIR_PATH):
            with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'w+') as f:
                pass

    def _update_ignored_dirs(self):
        with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'r') as f:
            for line in f.readlines():
                self.ignored_dirs.append(line)


    def _dig_for_docs(self, maxdepth = np.inf):
        if maxdepth and self.is_dir:
            dir_children = []
            file_children = []
            for fname in os.listdir(self.path):
                check_fname = not fname in self.ignored_dirs
                if check_fname:
                    for igdir in self.ignored_dirs:
                        predictive_path = self.path.joinpath(fname)
                        if re.search(igdir + '$', str(predictive_path)):
                            check_fname = False
                            self.process_warnings.append(self.structure_info(
                                f"{fname} was ignored because it is part of the .makedoc/ignored.mkdc file"
                            ))
                            break
                if check_fname:
                    child = DocParser(self.path.joinpath(fname))
                    if child.is_dir:
                        if len(os.listdir(child.path)) > self.MAX_DIR_SIZE or self.IGNORE_MARKER in os.listdir(child.path):
                            child.ignored = True
                            child.ignore_in_doc = True
                            child.ignore_in_struct = True
                            if self.IGNORE_MARKER in os.listdir(child.path):
                                os.remove(child.path.joinpath(self.IGNORE_MARKER))
                                with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'a') as f:
                                    f.write(child.path._str)
                                self.process_warnings.append(self.structure_info(
                                    f"{self.IGNORE_MARKER} found in {child.path._str}. It was removed and ./makedoc/{self.IGNORED_DIRS_FILENAME} was updated"
                                ))
                    if not child.ignore_in_struct:
                        if child.is_dir:
                            dir_children.append(child)
                        elif child.is_file:
                            file_children.append(child)
            dir_children.sort(key=lambda x:x.name)
            file_children.sort(key=lambda x:x.name)
            self.children = dir_children + file_children

    def structure_warning(self, warning_message:str):
        return '        [W]' + datetime.datetime.now().strftime(' %D %H:%M:%S ') + self.path._str + ' : ' + warning_message

    def structure_error(self, error_message:str):
        return '    [E] ' + datetime.datetime.now().strftime(' %D %H:%M:%S ') + self.path._str + ' : ' + error_message

    def structure_info(self, info_message:str):
        return '            [I] ' + datetime.datetime.now().strftime(' %D %H:%M:%S ') + self.path._str + ' : ' + info_message

    def _parse_doc(self):
        if self.is_dir:
            self._parse_dirdoc()
        elif self.is_file:
            if re.search(r'\.py$', self.name):
                try:
                    self._parse_as_py_file()
                except:
                    self.process_warnings.append(self.structure_error(
                        'The file could not be parsed. It has been ignored.'
                    ))
            elif re.search(r'\.md$', self.name):
                self._parse_as_md_file()
            else:
                # self.ignored = True
                self.process_warnings.append(self.structure_warning(
                    'The file was ignored because its extenstion was not recognised.'
                ))
        else:
            self.ignore_in_struct = True
            self.ignore_in_doc = True
            self.process_warnings.append(self.structure_error(
                'The file was ignored because it was not recognised either as a file nor a directory.'
            ))

    def _parse_as_py_file(self):
        with open(self.path, "r") as f:
            lines = f.readlines()
            info_began = False
            sep_type = None
            for l in lines:
                if not info_began:
                    if l == '"""\n':
                        sep_type = '"'
                        info_began = True
                    elif l == "'''\n":
                        sep_type = "'"
                        info_began = True
                else:
                    if l == 3*sep_type + '\n':
                        break
                    else:
                        self.docstrings.append(l)
            if not info_began:
                self.process_warnings.append(self.structure_warning(
                    'There is not beginning comment to this file. The doc remains empty.'
                ))
        self.md_strings = self.docstrings.copy()

    def _parse_as_md_file(self):
        if self.name in [self.DIRDOCNAME, self.OUTPUTFILE] + self.IGNORED_MD_FILES:
            self.ignore_in_doc = True
            self.ignore_in_struct = True
            self.process_warnings.append(self.structure_info(
                'The file was ignored as it is part of the whitelist defined by "[self.DIRDOCNAME, self.OUTPUTFILE] + self.IGNORED_MD_FILES"'
            ))
        with open(self.path, "r") as f:
            lines = f.readlines()
            if not lines:
                self.ignore_in_doc = True
                self.ignore_in_struct = False
                self.process_warnings.append(self.structure_warning(
                    'The file was ignored because it was empty.'
                ))
            elif lines[0] != '\n':
                self.md_strings = lines
            else:
                self.ignore_in_doc = True
                self.ignore_in_struct = False
                self.process_warnings.append(self.structure_info(
                    'The file was ignored because it started with an empty line.'
                ))

    def _parse_dirdoc(self):
        dirdocpath = self.path.joinpath(self.DIRDOCNAME)
        if not self.DIRDOCNAME in os.listdir(self.path):
            with open(dirdocpath, 'w+') as f:
                f.write(f'# {self.name}')
                f.close()
            self.process_warnings.append(self.structure_info(
                f'{self.DIRDOCNAME} file did not exist. Created one in {dirdocpath._str}.'
            ))
        with open(dirdocpath, "r") as f:
            self.md_strings = f.readlines()
            popindexes = []
            for idx, line in enumerate(self.md_strings):
                if re.search('# ' + self.name, line):
                    popindexes.append(idx)
            for idx in popindexes[::-1]:
                self.md_strings.pop(idx)
        if not self.md_strings:
            self.process_warnings.append(self.structure_warning(
                'The directory doc is empty.'
            ))

    def _erase_autodoc(self, recurse=True):
        if self.is_dir:
            if self.DIRDOCNAME in os.listdir(self.path):
                os.remove(self.path.joinpath(self.DIRDOCNAME))
            if self.OUTPUTFILE in os.listdir(self.path):
                os.remove(self.path.joinpath(self.OUTPUTFILE))
            if recurse:
                for child in self.children:
                    child._erase_autodoc(recurse = True)


    def __repr__(self):
        FCROSS = '└── '
        CROSSDIR = '├── '
        VERTLINE = '│   '
        # FCROSS = 'L__ '
        # CROSSDIR = '+-- '
        # VERTLINE = '|   '
        repr = self.name + '\n'
        for idx, child in enumerate(self.children):
            child_repr = child.__repr__().split('\n')
            new_child_repr = []
            if idx == len(self.children) - 1:
                VERTLINE = '    '
                CROSSDIR = FCROSS
            if child.is_dir:
                mrkr = 1
                for line in child_repr:
                    if line:
                        new_child_repr.append(mrkr*CROSSDIR + (1-mrkr)*VERTLINE + line + '\n')
                        mrkr = 0
                repr += ''.join(new_child_repr)
            elif child.is_file:
                repr += CROSSDIR + child.__repr__()
        return repr

    def get_file_struct(self, depth = np.inf):
        FCROSS = '└── '
        CROSSDIR = '├── '
        VERTLINE = '│   '
        # FCROSS = 'L__ '
        # CROSSDIR = '+-- '
        # VERTLINE = '|   '
        repr = self.name + self.is_dir*'/' + '\n'
        if depth:
            for idx, child in enumerate(self.children):
                child_repr = child.get_file_struct(depth=depth-1).split('\n')
                new_child_repr = []
                if idx == len(self.children) - 1:
                    VERTLINE = '    '
                    CROSSDIR = FCROSS
                if child.is_dir:
                    mrkr = 1
                    for line in child_repr:
                        if line:
                            new_child_repr.append(mrkr*CROSSDIR + (1-mrkr)*VERTLINE + line + '\n')
                            mrkr = 0
                    repr += ''.join(new_child_repr)
                elif child.is_file:
                    repr += CROSSDIR + child.__repr__()
        return repr

    def _get_doc(self,
                 doc_depth = 0,
                 block_quote_content = False):
        if self.ignore_in_doc:
            return []
        doc_lines = []
        doc_lines.append('#' * (1+doc_depth) + ' ' + self.name + '\n')
        if block_quote_content:
            for line in self.md_strings:
                doc_lines.append('>' + line)
            doc_lines.append('\n---\n')
        else:
            doc_lines += self.md_strings
        # doc_lines.append('\n---\n')
        return doc_lines

    def _get_children_doc(self,
                          doc_depth = 0,
                          max_depth = np.inf):
        doc_lines = []
        if doc_depth < max_depth+1:
            if doc_depth > 0:
                doc_lines+= self._get_doc(doc_depth=doc_depth,
                                          block_quote_content=True)
            if self.is_dir:
                for child in self.children:
                    doc_lines += child._get_children_doc(doc_depth=doc_depth + 1, max_depth=max_depth)
        return doc_lines

    def get_all_warnings(self):
        out = self.process_warnings.copy()
        if self.is_dir:
            for child in self.children:
                out += child.get_all_warnings()
        return out

    def makedoc(self,
                recurse = False,
                doc_depth = 1,
                file_structure_depth = 4,
                verbose = True,
                generate_log_report = False,
                first_call=True,
                update_README = False):
        if verbose and first_call:
            print(f'Starting the makedoc process from {self.path._str}')
        if self.is_dir:
            outfile_path = self.path.joinpath(self.OUTPUTFILE)
            file_strucure = '```\n' + self.get_file_struct(depth=file_structure_depth) + '```\n'
            file_doc_lines = self._get_doc()
            with open(outfile_path, 'w+') as f:
                for l in file_doc_lines:
                    f.write(l)
                f.write('\n<hr style="border:2px solid gray"> </hr>\n\n')
                f.write('## Structure \n')
                f.write(file_strucure)
                f.write('\n<hr style="border:2px solid gray"> </hr>\n\n')
                children_doc_lines = self._get_children_doc(max_depth=doc_depth)
                for l in children_doc_lines:
                    f.write(l)
                f.write(f'\n\n\n\n<sub>This doc was automatically generated with makedoc v{self.VERSION} on {datetime.datetime.now().strftime(" %D %H:%M:%S ")}')
        logs = self.get_all_warnings()
        if generate_log_report and first_call:
            if not 'logs' in os.listdir(self.path):
                log_folder_path = self.path.joinpath('logs')
                log_folder_path.mkdir()
                self.process_warnings.append(self.structure_warning(
                    'The logs folder did not exist. It was created at ' + log_folder_path._str
                ))
            log_report_path = self.path.joinpath('logs/autodoc_gen_report.log')
            with open(log_report_path, "w+") as f:
                f.write(f"makedoc_report built with makedoc v{self.VERSION} on " + datetime.datetime.now().strftime("%D %H:%M:%S \n\n"))
                for logline in logs:
                    f.write(logline + '\n')
        if recurse:
            for child in self.children:
                child.makedoc(recurse=True,
                              doc_depth=doc_depth,
                              first_call=False,
                              verbose=False,
                              file_structure_depth=file_structure_depth,
                              update_README=update_README)
        if self.is_dir and update_README and ('README.md' in os.listdir(self.path)):
            if 'README.md' in os.listdir(self.path):
                with open(self.path.joinpath(self.OUTPUTFILE), 'r') as autodoc_file:
                    with open(self.path.joinpath('README.md'), 'w+') as README_file:
                        lines = autodoc_file.readlines()
                        for l in lines:
                            README_file.write(l)
        if verbose:
            for warning in logs:
                print(warning)
            print("Makedoc process finished. The doc is ready.")

source_parser = DocParser(root_path,
               ignored_dirs=['venv',
                             '.git',
                             '.idea',
                             ],
               )
source_parser.makedoc(update_README=True,
                      generate_log_report=True
                      )

recursive_parser = DocParser(root_path.joinpath('src',),
                            )
recursive_parser.makedoc(recurse=True,
                         verbose=False,
                         update_README=True)