# Equalize_Cephalographs

Python functions to equalize the grayscale values of cephalographs

## Instructions

- Download & install Anaconda Python (https://www.anaconda.com/download). It's a big install, so it takes a while.
- (Optional) Install Sublime Text for editing .py` files (https://www.sublimetext.com/). Or use your preferred text editor.
- Open Anaconda shell
- Install packages (only do this once):
    - `conda install scikit-image`
    - `conda install pillow`
- Edit `Equalize_Histograms.py` lines 159-162
    - `rootDir`: Top level of directory to process.
    - `eq`: Suffix for equalized images
    - `ad_eq`: Suffix for adaptive equalized images
    - `ct`: Suffix for contrast stretching images
- `cd` to location where `Equalize_Histograms.py` is saved
    - `cd users\admin\Desktop\`
- `python Equalize_Histograms.py`
- Wait
