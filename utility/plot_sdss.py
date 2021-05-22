#######################################
# The purpose of this .py is to fetch #
# the data from SDSS's SQL database   #
# for any given RA, DEC, and CLASS.   #
#######################################

#####################
# IMPORT STATEMENTS #
#####################

from matplotlib import pyplot as plt
import numpy as np
from fetch_sdss import *

#############
# MAIN CODE #
#############

# We can use this to fetch the one hot and optionally 
# a colormapping associated with that one hot.
def get_one_hot(patch_of_sky):

    '''
        patch_of_sky -> the dataframe from SDSS that contains classes.
    '''

    # Get all of the classes and their unique occurrences.
    classes = patch_of_sky['class']
    unq_classes = pds.unique(classes)

    # Define a numpy array to store the Boolean values.
    one_hot = np.zeros((classes.shape[0], unq_classes.shape[0]), dtype = int)

    for idx, elem in enumerate(unq_classes):
        loc = elem == classes
        one_hot[:, idx] = loc

    return one_hot

def get_color_map(one_hot, obj_colors):
    obj_cmap = []

    if (type(obj_colors) != str) and (len(obj_colors) != len(unq_classes)):
        print('The size of the input colors does not match the size of the number of unique classes.\n')
        print('Returning just the one hot.')
        return one_hot

    else:
        for idx, _ in enumerate(classes):

            obj_cmap.append('')
            for jdx, _ in enumerate(unq_classes):
                if type(obj_colors) == str:
                    color = obj_colors
                else:
                    color = obj_colors[jdx]
                obj_cmap[idx] += one_hot[idx, jdx]*color

    




def plot_celestial_coordinates(patch_of_sky, obj_size = 100, obj_alpha = 1, obj_cmap = None):

    '''
        patch_of_sky -> the dataframe from SDSS that contains coordinates.
        obj_size -> the size of the objects for the plot.
        obj_alpha -> the transparency of the objects.
        obj_cmap -> the colors and sizes for the object.
    '''

    fig, ax = plt.subplots(1, 1)

    # Get the celestial coordinates.
    ra = patch_of_sky['ra']
    dec = patch_of_sky['dec']

    # Checking to see if the object's colormapping is defined.
    if obj_cmap is None:
        ax.scatter(ra, dec, alpha = obj_alpha, s = obj_size, c = 'gold')
    else:
        ax.scatter(ra, dec, alpha = obj_alpha, s = obj_size, c = obj_cmap)

    # Labeling the axes and giving it a title.
    ax.set_ylabel('declination, degrees', fontsize = 12)
    ax.set_xlabel('right ascension, degrees', fontsize = 12)
    ax.set_title('celestial coordinates of the patch', fontsize = 14)

    return fig, ax
ra = (0, .1)
dec = ra
print('red'*0)
df = get_sky_patch(ra, dec)

get_one_hot(df, ['red', 'blue', 'green'])

