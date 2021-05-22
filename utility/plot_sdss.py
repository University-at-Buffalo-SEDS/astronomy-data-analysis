#######################################
# The purpose of this .py is to fetch #
# the data from SDSS's SQL database   #
# for any given RA, DEC, and CLASS.   #
#######################################

#####################
# IMPORT STATEMENTS #
#####################

from matplotlib import pyplot as plt
from fetch_sdss import *

#############
# MAIN CODE #
#############

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
