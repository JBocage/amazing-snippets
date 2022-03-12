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

For adding figures, you need to put your figure in .makedoc/imgs
Then from any script command, you can include it by writing `@img:img_filename` at the beginning of the line
"""

import pathlib
import os
import shutil
import re
import time
import datetime
import sys
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

    VERSION = '1.1.5'

    MAKEDOC_DIR_PATH = pathlib.Path(os.path.abspath(os.path.join(__file__,
                                                            '../.makedoc')))
    ROOT_PATH = pathlib.Path(os.path.abspath(os.path.join(__file__,
                                              '..',
                                              )))
    IGNORED_DIRS_FILENAME = 'ignored.mkdc'

    class Log_message():

        WARNING = 3
        INFO = 2
        ERROR = 1

        def __init__(self,
                     type,
                     path,
                     message):
            if not type in [self.WARNING, self.INFO, self.ERROR]:
                raise ValueError(f'Specified type is not valid.')
            self.type = type
            self.path = path
            self.time = datetime.datetime.now()
            self.message = message

        def __repr__(self):
            if self.type == self.ERROR:
                token = '[E]'
            elif self.type == self.WARNING:
                token = '[W]'
            else:
                token = '[I]'
            return token + self.time.strftime(' %D %H:%M:%S at ' + self.path._str + ' : ') + self.message

    def __init__(self,
                 path:pathlib.Path,
                 ignored_dirs=[],
                 ignore___init__doc=True,
                 initialiser=True,
                 repack=False
                 ):
        self._init_makedoc_dir()

        self.is_first = initialiser
        self.name = path.name
        self.is_dir = path.is_dir()
        self.is_file = path.is_file()
        self.path = path.absolute()
        self.repack=repack
        self.ignored = False
        self.ignore_in_doc = False
        self.ignore_in_struct = False
        self.ignore___init__doc = ignore___init__doc

        self.IGNORED_DIRS += ignored_dirs
        self.ignored_dirs_and_files = []
        self._update_ignored_dirs_and_files()

        self.children = []

        self.docstrings = []
        self.md_strings = []

        self.process_warnings = []
        self.logs = []

        self._check_if_ignored()
        if not self.ignore_in_doc:
            self.unpack_doc(recurse=False)
            self._parse_doc()
        if self.ignore_in_doc and self.ignore_in_struct:
            pass
        else:
            self._dig_for_docs(maxdepth=3)

        if repack and self.is_first:
            self.pack_doc()
            # self._erase_autodoc()

    def _init_makedoc_dir(self):
        self.MAKEDOC_DIR_PATH.mkdir(exist_ok=True)
        self.MAKEDOC_DIR_PATH.joinpath('imgs').mkdir(exist_ok=True)
        if not self.IGNORED_DIRS_FILENAME in os.listdir(self.MAKEDOC_DIR_PATH):
            with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'w+') as f:
                pass

    def _update_ignored_dirs_and_files(self):
        with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'r') as f:
            for line in f.readlines():
                if line !='\n':
                    self.ignored_dirs_and_files.append(line)

    def _get_partial_path(self):
        fullpath = self.path.__str__()
        root_path = self.ROOT_PATH.__str__()
        partial_path = fullpath[len(root_path):]
        return  partial_path

    def _check_if_ignored(self):

        def check_ign_dir_and_files_list():
            for path in self.ignored_dirs_and_files:
                if re.match(path.strip(), self._get_partial_path()):
                    return True
                if re.match('/'+path.strip(), self._get_partial_path()):
                    return True
                if re.match(path.strip(), self.path._str):
                    return True
            return False

        type = 'file' * int(self.is_file) + 'directory' * int(self.is_dir)

        if check_ign_dir_and_files_list():
            self.ignore_in_doc = True
            self.ignore_in_struct = True
            self.log_info(f'The {type} was ignored because it was mentioned in .makedoc/{self.IGNORED_DIRS_FILENAME}')
        elif self.name in self.IGNORED_DIRS:
            self.ignore_in_doc = True
            self.ignore_in_struct = True
            self.log_info(f'The {type} was ignored because it was mentioned in self.IGNORED_DIRS_FILENAME')
        else:
            if self.is_dir:
                if len(os.listdir(self.path)) > self.MAX_DIR_SIZE:
                    self.ignore_in_doc = True
                    self.ignore_in_struct = True
                    self.log_warning('The directory was ignored because it contained to many files')
                elif self.IGNORE_MARKER in os.listdir(self.path):
                    self.ignore_in_doc = True
                    self.ignore_in_struct = True
                    self.log_info(f'A {self.IGNORE_MARKER} was found in the directory. The marker was deleted and the .makedoc/{self.IGNORED_DIRS_FILENAME} file was updated.')
                    os.remove(self.path.joinpath(self.IGNORE_MARKER))
                    with open(self.MAKEDOC_DIR_PATH.joinpath(self.IGNORED_DIRS_FILENAME), 'a') as f:
                        f.write('\n' + self.path._str)

            elif self.is_file:
                if self.ignore___init__doc and self.name == "__init__.py":
                    self.ignore_in_doc = True
                    self.ignore_in_struct = False
                    self.log_info(f'The file was ignored as it is recognised as a "__init__.py" file.')
                if self.name in [self.DIRDOCNAME, self.OUTPUTFILE] + self.IGNORED_MD_FILES:
                    self.ignore_in_doc = True
                    self.ignore_in_struct = True
                    self.log_info(f'The file was recognised as a file to ignore.')

    def pack_doc(self):
        if self.is_dir:
            dest_dir_path = self.path.joinpath(self.MAKEDOC_DIR_PATH, 'packed_doc/'+self._get_partial_path())
            dest_dir_path.mkdir(parents=True,
                                exist_ok=True)
            shutil.copyfile(self.path.joinpath(self.DIRDOCNAME), dest_dir_path.joinpath(self.DIRDOCNAME))
            for child in self.children:
                child.pack_doc()
        self._erase_autodoc()

    def unpack_doc(self,
                   recurse=True):
        if self.is_dir:
            dirdoc_path = self.path.joinpath(self.MAKEDOC_DIR_PATH,
                                             'packed_doc/'+self._get_partial_path()+'/'+self.DIRDOCNAME)
            if dirdoc_path.exists() and not self.path.joinpath(self.DIRDOCNAME).exists():
                shutil.copyfile(dirdoc_path, self.path.joinpath(self.DIRDOCNAME))
            if recurse:
                for child in self.children:
                    child.unpack_doc()

    def _dig_for_docs(self, maxdepth = np.inf):
        if maxdepth and self.is_dir:
            dir_children = []
            file_children = []
            for fname in os.listdir(self.path):
                child = DocParser(self.path.joinpath(fname),
                                  initialiser=False)
                if not child.ignore_in_struct:
                    if child.is_dir:
                        dir_children.append(child)
                    elif child.is_file:
                        file_children.append(child)
            dir_children.sort(key=lambda x:x.name)
            file_children.sort(key=lambda x:x.name)
            self.children = dir_children + file_children

    def log_warning(self, message):
        self.logs.append(self.Log_message(self.Log_message.WARNING,
                                          self.path,
                                          message))

    def log_info(self, message):
        self.logs.append(self.Log_message(self.Log_message.INFO,
                                          self.path,
                                          message))

    def log_error(self, message):
        self.logs.append(self.Log_message(self.Log_message.ERROR,
                                          self.path,
                                          message))

    def _parse_doc(self):
        if not self.ignore_in_doc:
            if self.is_dir:
                self._parse_dirdoc()
            elif self.is_file:
                if re.search(r'\.py$', self.name):
                    try:
                        self._parse_as_py_file()
                    except:
                        self.log_warning('The file could not be parsed. It has been ignored.')
                elif re.search(r'\.md$', self.name):
                    self._parse_as_md_file()
                else:
                    self.log_warning('The file was ignored because its extenstion was not recognised.')
            else:
                self.ignore_in_struct = True
                self.ignore_in_doc = True
                self.log_warning('The file was ignored because it was not recognised either as a file nor a directory.')

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
                self.log_warning('There is not beginning comment to this file. The doc remains empty.')
        for line in self.docstrings:
            if re.search(r'(?<=^@img:)\w+\.\w+', line):
                img_name = re.search(r'(?<=^@img:)\w+\.\w+', line)[0]
                img_dir_path=self.MAKEDOC_DIR_PATH.joinpath('imgs/')
                if img_name in os.listdir(img_dir_path):
                    img_path = img_dir_path.joinpath(img_name)
                    self.md_strings.append(f'<img src="{img_path.__str__()}" alt="drawing" width="400"/>\n')
                else:
                    self.log_warning(f'Image named {img_name} was not found in {img_dir_path}.')
            else:
                self.md_strings.append(line)

    def _parse_as_md_file(self):
        with open(self.path, "r") as f:
            lines = f.readlines()
            if not lines:
                self.ignore_in_doc = True
                self.ignore_in_struct = False
                self.log_warning('The file was ignored because it was empty.')
            elif lines[0] != '\n':
                self.md_strings = lines
            else:
                self.ignore_in_doc = True
                self.ignore_in_struct = False
                self.log_info('The file was ignored because it started with an empty line.')

    def _parse_dirdoc(self):
        dirdocpath = self.path.joinpath(self.DIRDOCNAME)
        if not self.DIRDOCNAME in os.listdir(self.path):
            with open(dirdocpath, 'w+') as f:
                f.write(f'# {self.name}')
                f.close()
            self.log_info(f'{self.DIRDOCNAME} file did not exist. Created one in {dirdocpath._str}.')
        with open(dirdocpath, "r") as f:
            self.md_strings = f.readlines()
            popindexes = []
            for idx, line in enumerate(self.md_strings):
                if re.search('^# ' + self.name, line):
                    popindexes.append(idx)
            for idx in popindexes[::-1]:
                self.md_strings.pop(idx)
        if not self.md_strings:
            self.log_warning('The directory doc is empty.')

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

    def get_all_logs(self):
        out = []
        self.logs.sort(key=lambda x:x.type)
        for log in self.logs:
            out.append(log)
        if self.is_dir:
            for child in self.children:
                out += child.get_all_logs()
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
        logs = self.get_all_logs()
        logs.sort(key=lambda x:-x.type)
        if generate_log_report and first_call:
            log_folder_path = self.MAKEDOC_DIR_PATH.joinpath('logs')
            if not log_folder_path.exists():
                log_folder_path.mkdir()
                self.log_info('The logs folder did not exist. It was created at ' + log_folder_path._str)
            log_report_path = log_folder_path.joinpath('autodoc_gen_report.log')

            infos = [log for log in logs if log.type==self.Log_message.INFO]
            warnings = [log for log in logs if log.type == self.Log_message.WARNING]
            errors = [log for log in logs if log.type==self.Log_message.ERROR]

            with open(log_report_path, "w+") as f:
                f.write(f"makedoc_report built with makedoc v{self.VERSION} on " + datetime.datetime.now().strftime("%D %H:%M:%S \n"))
                f.write(100*'=' + '\n\n')
                f.write(f"    ERRORS   : {len(errors)} \n"
                        f"    WARNINGS : {len(warnings)} \n"
                        f"    INFOS    : {len(infos)} \n\n"
                        )
                f.write(100*'=' + '\n\n')
                if errors:
                    for errno, errorlog in enumerate(errors):
                        f.write(f"    ERROR #{errno+1}/{len(errors)}\n"
                                f"            - file : {errorlog.path}\n"
                                f"            - time : {errorlog.time.strftime('%D %H:%M:%S')}\n"
                                f"        - msg : {errorlog.message} \n\n\n")
                    f.write(100*'-' + '\n\n')
                if warnings:
                    for warno, warlog in enumerate(warnings):
                        f.write(f"    WARNING #{warno+1}/{len(warnings)}\n"
                                f"            - file : {warlog.path}\n"
                                f"            - time : {warlog.time.strftime('%D %H:%M:%S')}\n"
                                f"        - msg : {warlog.message} \n\n\n")
                    f.write(100*'-' + '\n\n')
                if infos:
                    for infno, inflog in enumerate(infos):
                        f.write(f"    INFO #{infno+1}/{len(infos)}\n"
                                f"            - file : {inflog.path}\n"
                                f"            - time : {inflog.time.strftime('%D %H:%M:%S')}\n"
                                f"        - msg : {inflog.message} \n\n\n")
                    f.write(100*'-' + '\n\n')
                for log in logs:
                    f.write(log.__str__() + '\n')
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
        if self.repack:
            self._erase_autodoc()
        if verbose:
            for warning in logs:
                print(warning)
            print("Makedoc process finished. The doc is ready.")

if __name__ == '__main__':

    source_parser = DocParser(root_path,
                   ignored_dirs=['venv',
                                 '.git',
                                 '.idea',
                                 ],
                   repack=True
                   )
    source_parser.makedoc(update_README=True,
                          generate_log_report=True,
                          recurse=True
                          )
