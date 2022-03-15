# amazing-snippets

Welcome to the **amazing-snippets** project !

This project aims to gather all intersting, useful of _amazing_ snippets I could  find 
over the internet and my code during my programmer experience.

This is here to help people keep their recurrent code snippets. 

I hope you will like it !
<hr style="border:2px solid gray"> </hr>

## Structure 
```
amazing-snippets/
├── doc/
│   └── imgs/
│       ├── color_bar_integration_output.png
│       └── plot_contour_and_line_output.png
├── src/
│   ├── colors/
│   │   ├── colorbars/
│   │   ├── access_xkcd.py
│   │   └── display_mpl_colors.py
│   ├── files_manip/
│   │   ├── input/
│   │   ├── output/
│   │   └── merge_pdfs.py
│   ├── markdown/
│   │   └── cheat_sheet_1.md
│   ├── matplotlib/
│   │   ├── 3D_plots/
│   │   │   └── plot_contour_and_line.py
│   │   └── color_bar_integration.py
│   └── pandas/
│       ├── data/
│       │   └── moscow_real_estate_sale.csv
│       └── make_categories.py
└── makedoc.py
```

<hr style="border:2px solid gray"> </hr>

## doc
>
>The **doc** directory contains all the documentation-related files.
---
## src
>
>The **src** directory basically contains all the code snippets of the project. This is where you will find all the useful stuff !
---
## makedoc.py
>> author: JBocage
>
>This script automatically generates the documentation skeleton for the project.
>
>It aims to function from every source directory. It is easy to use it. An sample of what is contained in the file is given here.
>
>```python
>    source_parser = DocParser(root_path,
>                   ignored_dirs=['venv',
>                                 '.git',
>                                 '.idea',
>                                 ],
>                   repack=True
>                   )
>    source_parser.makedoc(update_README=True,
>                          generate_log_report=True,
>                          recurse=True
>                          )
>```
>
>For adding figures, you need to put your figure in .makedoc/imgs
>Then from any script command, you can include it by writing `@img:img_filename` at the beginning of the line

---




<sub>This doc was automatically generated with makedoc v1.1.6 on  03/15/22 12:55:22 