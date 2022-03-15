# files_manip

The **files_manip** directory aims to gather scripts that will help you merge and convert files.

It may even contain some zip file cracking script someday...
<hr style="border:2px solid gray"> </hr>

## Structure 
```
files_manip/
├── input/
├── output/
└── merge_pdfs.py
```

<hr style="border:2px solid gray"> </hr>

## input
>
>This shall contain every input that are processed by the files_manip scripts.
---
## output
>
>files_manip script shall output their resulting files here !
---
## merge_pdfs.py
>> inspiration-url: https://caendkoelsch.wordpress.com/2019/05/10/merging-multiple-pdfs-into-a-single-pdf/
>
>> author: JBocage
>
>This code is largely inspired from a snippet found on internet. It provides with a tool to merge all pdfs that are contained in
>./input and save the resulting pdf into ./output. The order is not under control yet.
>
>To adapt this code for other uses, you can modify the config part (see below)
>
>```python
>################################
>########### Config #############
>################################
>verbose = True
>
>inputs_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../input')))
>output_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../output')))
>
>sorting_key = lambda x:x
>
>outfilename = 'out' + '.pdf'
>################################
>```

---




<sub>This doc was automatically generated with makedoc v1.1.6 on  03/15/22 15:47:24 