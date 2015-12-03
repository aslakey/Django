#_______Consolidated Code for Project
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.measure import regionprops
from skimage import restoration
from skimage import measure
from skimage.color import label2rgb
import matplotlib.patches as mpatches
import os
import skimage
from skimage import io
from skimage.viewer import ImageViewer
from scipy.misc import toimage
from skimage import feature
import scipy.ndimage as ndi

#Read file into array as greyscale (need to eventually change to user uploaded image)
filename = os.path.join(skimage.data_dir, 'quote_image.png') #change file name accordingly
chk = io.imread(filename,as_grey = True) #returns greyscale image

#Process one Denoise and Increase Contrast
image = restoration.denoise_tv_chambolle(chk, weight=0.1) #Denoises using total variation

#Process two Finding Objects: http://scikit-image.org/docs/dev/auto_examples/plot_label.html
#canny filter (lower sigma shows more detail)
edges = feature.canny(image, sigma=1) 
#segment the image based on edges using http://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
segmentation = ndi.binary_fill_holes(edges)
labels, _ = ndi.label(segmentation)
#overlay these labels on colored image 
image_label_overlay = label2rgb(labels, image=chk)

#Process 3 Collect these regions filtering out small ones:
'''show image in plot with overlayed regions
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
ax.imshow(image_label_overlay)
'''
candidates = []
for region in regionprops(labels):

    # skip small images
    if region.area < 200:
        continue

    # draw rectangle around each region
    minr, minc, maxr, maxc = region.bbox
    candidates.append([minr,minc,maxr,maxc])
    '''
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)
plt.show()
    '''


#Process 4: decide if Region is a character or not!
