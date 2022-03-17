"""
> inspiration-url: https://caendkoelsch.wordpress.com/2019/05/10/merging-multiple-pdfs-into-a-single-pdf/

> author: JBocage

This code is largely inspired from a snippet found on internet. It provides with a tool to merge all pdfs that are contained in
./input and save the resulting pdf into ./output. The order is not under control yet.

To adapt this code for other uses, you can modify the config part (see below)

@snip:config

"""
import os
import re

import PyPDF2
import pathlib

# @begin:config
################################
########### Config #############
################################
verbose = True

inputs_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../input')))
output_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../output')))

sorting_key = lambda x:x

outfilename = 'out' + '.pdf'
################################
# @end:config

def merge_pdfs(inputs_path = inputs_path,
               output_path = output_path,
               outfilename=outfilename,
               verbose=verbose,
               sorting_key=sorting_key):
    inputs_path.mkdir(exist_ok=True,
                      parents=True)

    pdfWriter = PyPDF2.PdfFileWriter()

    nothing_written = True
    taken_pdfs = []
    opened_files = []
    listdir = os.listdir(inputs_path)
    listdir.sort(key=sorting_key)
    for fname in listdir:
        if re.search(r'\.pdf$', fname):
            if verbose:
                print(f"Found {fname} to be merged.")
            pdfFile = open(inputs_path.joinpath(fname), 'rb')
            opened_files.append(pdfFile)
            pdfReader = PyPDF2.PdfFileReader(pdfFile)
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            taken_pdfs.append(fname)
            nothing_written = False


    if nothing_written and verbose:
        print("No PDF was found")
    elif verbose:
        print(f"Writing output pdf in {output_path.joinpath(outfilename)}")
        with open(output_path.joinpath(outfilename), 'wb') as pdfOutfile:
            pdfWriter.write(pdfOutfile)
    for file in opened_files:
        file.close()

    if verbose and not nothing_written:
        print("Files that were merged:")
        for fname in taken_pdfs:
            print("    " + fname)
        ans = input("Would you like to erase them ? [y/n] >")
        if ans == 'y':
            print("Removing files...")
            for fname in taken_pdfs:
                os.remove(inputs_path.joinpath(fname))
            print("Done !")

if __name__=='__main__':
    merge_pdfs()