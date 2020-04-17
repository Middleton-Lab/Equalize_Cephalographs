# coding: utf-8

# Opens and resaves all tiff files in the current directory. This can be useful
# for fixing damaged tiff files written by other programs.

# Requires that imagemagick be installed and mogrify available in the PATH.

from subprocess import call
import shlex
import glob
import sys
import subprocess

for filename in glob.glob('./**', recursive=True):
    if filename.endswith('.tif'):
        print(shlex.quote(filename))
        if sys.platform == 'win32':
            subprocess.Popen(['mogrify', '-format', 'tif', filename])
        else:
            call('mogrify ' + '-format ' + 'tif ' + shlex.quote(filename), shell=True)
