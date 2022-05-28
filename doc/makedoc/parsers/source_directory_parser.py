from .directory_parser import DirectoryParser

class SourceDirectoryParser(DirectoryParser):

    def __init__(self, path):

        self._init_makedoc_file_structure()
        super(SourceDirectoryParser, self).__init__(path=path,
                                                    root_path=path)
        # self._mine_for_doc()

    def get_partial_path(self):
        return ''

    def is_ignored(self) -> bool:
        return False

    def save_readme(self):
        with open(self.path/'readme.md', 'w+') as f:
            f.write(self.get_doc_file_content())
        return

    def _init_makedoc_file_structure(self):

        self.Paths.packed_doc.mkdir(exist_ok=True)      # Create the packed doc folder
        self.Paths.config.mkdir(exist_ok=True)          # Create the config folder

        # Ignroed files and directories initialisation
        if not self.Paths.ignored_path.exists():
            with open(self.Paths.ignored_path, 'w+') as f:
                f.write("###################################################\n"
                        "# This file shall contain all ignored directories\n"
                        "# and files for this project.\n"
                        "# \n"
                        "# Every path that matches those relative or absolute\n"
                        "# paths are to be ignored in both structure representation\n"
                        "# and README documentation.\n"
                        "###################################################\n"
                        "\n"
                        "venv/\n"
                        "makedoc\n"
                        ".idea\n"
                        ".git\n"
                        ".makedoc\n"
                        "doc/makedoc/\n"
                        "doc/imgs/\n"
                        "\n"
                        "###################################################\n"
                        "# AUTO ADDED:\n")

        if not self.Paths.ignored_every.exists():
            with open(self.Paths.ignored_every, 'w+') as f:
                f.write("###################################################\n"
                        "# This file shall contain all ignored directories\n"
                        "# and files for this project.\n"
                        "# \n"
                        "# Every location or directory which name matches one\n"
                        "# that is provided here shall be ignored\n"
                        "###################################################\n"
                        "\n"
                        "README.md\n"
                        "__pycache__\n"
                        "\n"
                        "###################################################\n"
                        "# AUTO ADDED:\n")

        if not self.Paths.ignored_extensions.exists():
            with open(self.Paths.ignored_extensions, 'w+') as f:
                f.write("###################################################\n"
                        "# This file shall contain all ignored file \n"
                        "# extensions for this project.\n"
                        "# \n"
                        "# Every file the extension of which matches one\n"
                        "# that is provided here shall be ignored\n"
                        "###################################################\n"
                        "\n"
                        "pdf\n"
                        "txt\n")
