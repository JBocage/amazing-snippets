# colorbars

Well I've spent so much time looking for the right way to build custom colorbars
from my imagination and from screenshots. 

This directory aims to gather the most simple scripts to do all that messy stuff! 
<hr style="border:2px solid gray"> </hr>

## Structure 
```
colorbars/
├── custom_bars/
├── input/
├── makebar_from_list.py
└── makebar_from_screenshot.py
```

<hr style="border:2px solid gray"> </hr>

## custom_bars
>
>This directory gathers custom colorbars that were created by this project's scripts.
---
## input
>
>This directory shall contain all the input files that are to be used in the
>following colorbars scripts
---
## makebar_from_list.py
>> author: JBocage
>
>This script aims to provide an efficient tool to design colorbars by manually chosing the color at predified positions.
>
>The color organisation can be chosen in the underlying part
>
>```python
>save_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../custom_bars')))
>
>clist = [
>    (0, 'white'),
>    (.2, 'orange'),
>    (.3,'blue'),
>    (1, 'black'),
>]
>
>interpolation_mode='linear'
>```

---
## makebar_from_screenshot.py
>> author: JBocage
>
>This script aims to provide an efficient tool to design colorbars from screenshots.
>
>A minimal configuration is done in the underlying part.
>
>```python
>save_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../custom_bars')))
>input_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../input')))
>
>interpolation_mode='linear'
>```
>
>When saving a colorbar, the script also erases the source screenshot.

---




<sub>This doc was automatically generated with makedoc v1.1.7 on  03/21/22 16:16:40 