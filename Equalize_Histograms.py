# coding: utf-8

# Equalize Histograms
#
# Improves the contrast range of a black and white image (radiograph) by
# applying three transformations:
#       1. Histogram equalization
#       2. Adaptive histogram equalization
#       3. Contrast stretching
#
# Following:
#   http://scikit-image.org/docs/dev/auto_examples/plot_equalize.html
#   http://stackoverflow.com/questions/18446804/python-read-and-write-tiff-16-bit-three-channel-colour-images
#   http://en.wikipedia.org/wiki/Histogram_equalization
#   http://homepages.inf.ed.ac.uk/rbf/HIPR2/stretch.htm
#
# Requires: scikit-image, tifffile, numpy, matplotlib, pillow (for writing jpg)
#
# To do
#   Collections.namedtuple
#   less fragile function returns
#   Convert to cython?
#   Better handle user input
#   logging for better logging

def plot_img_and_hist(img, axes, bins=65536):
    """
    Plot an image along with its histogram and cumulative histogram.
    """
    from skimage import img_as_float, exposure
    import matplotlib
    import matplotlib.pyplot as plt

    img = img_as_float(img)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(img, cmap=plt.cm.gray)
    ax_img.set_axis_off()
    ax_img.set_adjustable('box-forced')

    # Display histogram
    ax_hist.hist(img.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(img, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    collected = gc.collect()
    # print("plot_img_and_hist: collected %d objects." % collected)

    return ax_img, ax_hist, ax_cdf


def equalize_image(infile):
    """
    Load and perform three different kinds of histogram equilization.
    """
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    from skimage import data, img_as_ubyte
    from skimage import exposure, io, color

    import warnings
    import gc

    matplotlib.rcParams['font.size'] = 8

    # %matplotlib inline

    # Load image
    img = data.imread(infile)

    # Contrast stretching
    p_lower, p_upper = np.percentile(img, (2, 95))
    img_rescale = exposure.rescale_intensity(img,
                                             in_range=(p_lower, p_upper))

    # Equalization
    img_eq = exposure.equalize_hist(img)

    # Adaptive Equalization
    img_adapteq = exposure.equalize_adapthist(img,
                                              clip_limit=0.1,
                                              nbins=2**16)

    # Display results
    fig = plt.figure(figsize=(10, 8))
    axes = np.zeros((2, 4), dtype=np.object)
    axes[0, 0] = fig.add_subplot(2, 4, 1)
    for i in range(1, 4):
        axes[0, i] = fig.add_subplot(2, 4, 1+i,
                                     sharex=axes[0, 0],
                                     sharey=axes[0, 0])
    for i in range(0, 4):
        axes[1, i] = fig.add_subplot(2, 4, 5+i)

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img, axes[:, 0])
    ax_img.set_title('Low contrast image')

    y_min, y_max = ax_hist.get_ylim()
    ax_hist.set_ylabel('Number of pixels')
    ax_hist.set_yticks(np.linspace(0, y_max, 5))

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_rescale, axes[:, 1])
    ax_img.set_title('Contrast stretching')

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_eq, axes[:, 2])
    ax_img.set_title('Histogram equalization')

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_adapteq, axes[:, 3])
    ax_img.set_title('Adaptive equalization')

    ax_cdf.set_ylabel('Fraction of total intensity')
    ax_cdf.set_yticks(np.linspace(0, 1, 5))

    # prevent overlap of y-axis labels
    with warnings.catch_warnings():  # Ignore warning about tight layout
        warnings.simplefilter("ignore")
        fig.tight_layout()
    plt.savefig(infile[:-4] + '_diag.pdf')
    plt.close(fig)

    # Convert to 8 bit and add color channels
    img_eq = color.gray2rgb((img_eq * 2**8).astype(np.uint8, copy=False))
    img_adapteq = color.gray2rgb((img_adapteq * 2**8).astype(np.uint8,
                                                             copy=False))

    with warnings.catch_warnings():  # Ignore warning about 16 bit to 8 bit
        warnings.simplefilter("ignore")
        img_rescale = color.gray2rgb(img_as_ubyte(img_rescale))

    collected = gc.collect()
    # print("equalize_image: collected %d objects." % collected)

    # Consider dictionary {'img_eq':img_eq, 'img_adapteq':img_adapteq, 'img_rescale':img_rescale}
    return img_eq, img_adapteq, img_rescale

###############################################################################

# To run a single file
# infile = './path_to_file/Filename.tif'
# img_eq_color, img_adapteq_color, img_rescale_color = equalize_image(infile)

import os
from skimage import io
import time
import gc

# Set the directory you want to start from
rootDir = './path_to_directory'
eq = '_Equalization'
ad_eq = '_Adaptive_Equalization'
ct = '_Contrast_Stretching'

# Suffixes
file_type = '.jpg'

main_start = time.time()
counter = 0

for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):

    print('Found directory: %s' % dirName)

    for fname in fileList:

        if fname.endswith('.tif'):

            # Check that directories exist, if not make them
            if not os.path.isdir(os.path.join(dirName, 'Eq')):
                os.mkdir(os.path.join(dirName, 'Eq'))
            if not os.path.isdir(os.path.join(dirName, 'Ad_Eq')):
                os.mkdir(os.path.join(dirName, 'Ad_Eq'))
            if not os.path.isdir(os.path.join(dirName, 'Contrast')):
                os.mkdir(os.path.join(dirName, 'Contrast'))

            print()
            start_time = time.time()

            print("Processing image:", fname)

            # Run equalizations and assign variables
            img_eq, img_adapteq, img_rescale = equalize_image(os.path.join(dirName, fname))

            # Write files
            io.imsave(os.path.join(dirName, 'Eq', fname[:-4]) + eq + file_type, img_eq)
            io.imsave(os.path.join(dirName, 'Ad_Eq', fname[:-4]) + ad_eq + file_type, img_adapteq)
            io.imsave(os.path.join(dirName, 'Contrast', fname[:-4]) + ct + file_type, img_rescale)

            end_time = time.time()
            m, s = divmod(end_time - start_time, 60)
            time_str = "%02d:%02d" % (m, s)
            print("Time elapsed: %s" % time_str)
            counter += 1
            collected = gc.collect()
            #print("Outer loop: collected %d objects." % collected)

main_end = time.time()
m, s = divmod(main_end - main_start, 60)
h, m = divmod(m, 60)
time_str = "%02d:%02d:%02d" % (h, m, s)
print()
print("Total time elapsed: %s" % time_str )
print("%s images processed" % str(counter))
collected = gc.collect()
# print("Finishing: collected %d objects." % collected)
