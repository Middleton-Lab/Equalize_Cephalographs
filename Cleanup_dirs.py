# coding: utf-8

# Clean up temporary and unneeded output files from inage equalizaation.

import os
import shutil

# Set the directory you want to start from
rootDir = './my_root_directory'

for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):

    for fname in fileList:
        if fname.endswith('diag.pdf'):
            os.remove(os.path.join(dirName, fname))

for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):

    print('Found directory: %s' % dirName)

    if 'Ad_Eq' in dirName:
        shutil.rmtree(dirName)
    if 'Contrast' in dirName:
        shutil.rmtree(dirName)
    if 'Eq' in dirName:
        shutil.rmtree(dirName)
