# amazing-snippets

Welcome to the _amazing snippets_ repository !

This repository aims to gather all amazing, useful or funny code snippets I could find accros
my projects and internet research !
<hr style="border:2px solid gray"> </hr>

## Structure 
```
amazing-snippets/
├── logs/
├── src/
│   ├── colors/
│   │   ├── colorbars/
│   │   ├── access_xkcd.py
│   │   └── display_mpl_colors.py
│   ├── markdown/
│   │   └── cheat_sheet_1.md
│   └── matplotlib/
│       └── color_bar_integration.py
└── makedoc.py
```

<hr style="border:2px solid gray"> </hr>

## logs
>
>The **logs** directory is here for all logging functions to save their outputs. It is more
>practical that _'amazing'_.
---
## src
>
>The **src** directory gathers all the snippets of interest.
---
## makedoc.py
>> author: JBocage
>
>This script automatically generates the documentation skeleton for the project.
>
>It aims to function from every source directory. It is easy to use it. An sample of what is contained in the file is given here.
>
>```python
>
>root_path = pathlib.Path(os.path.abspath(os.path.join(__file__,'..',)))     # initialise the source path
>
>source_parser = DocParser(root_path,                                        # create the parser
>               ignored_dirs=['venv',
>                             '.git',
>                             '.idea',
>                             ],
>               )
>source_parser.makedoc(update_README=True,                                   # generate the doc
>                      )
>
>recursive_parser = DocParser(root_path.joinpath('src',),                    # another example of parser
>                            )
>recursive_parser.makedoc(recurse=True,                                      # another example of doc generation call
>                         verbose=False)
>```
>
>For adding figures, you need to put your figure in .makedoc/imgs
>Then from any script command, you can include it by writing `@img:img_filename` at the beginning of the line

---




<sub>This doc was automatically generated with makedoc v1.1.3 on  03/08/22 08:52:53 