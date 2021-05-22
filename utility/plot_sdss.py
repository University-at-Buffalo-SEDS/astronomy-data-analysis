#######################################
# The purpose of this .py is to plot  #
# the data from SDSS's SQL database.  #
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
    one_hot = np.zeros((classes.shape[0], unq_classes.shape[0]), dtype = bool)

    # Iterating over to assign the binary values to the one-hot.
    for idx, elem in enumerate(unq_classes):

        # The locations where our current classes is equivalent
        # to all of the classes of the data.  This is True or False.
        loc = elem == classes

        one_hot[:, idx] = loc

    return one_hot

# We can use this to generate a colormapping for the celestial objects.
def get_color_map(one_hot, obj_colors):

    '''
        one_hot -> the one hot encoding of the data.
        obj_colors -> the colors by which the data will be mapped.
    '''

    # Storing the colors.
    obj_cmap = []

    # Dimensions for iterative purposes.
    num_classes = one_hot.shape[0]
    num_unq_classes = one_hot.shape[1]

    # Checking to make sure that the input is the same shape as 
    # the number of unique classes for indexing purposes.
    if (type(obj_colors) != str) and (len(obj_colors) != num_unq_classes):
        print('The size of the input colors does not match the size of the number of unique classes.')
        return None

    else:
        for idx in range(num_classes):
            
            # We initialize the class by index.
            obj_cmap.append('')

            for jdx in range(num_unq_classes):

                # Setting the color for string multiplication.
                if type(obj_colors) == str:
                    color = obj_colors
                else:
                    color = obj_colors[jdx]
                
                # If one_hot[idx, jdx] is 0, then it appends an empty string.
                # Otherwise, if it's 1, then it appends the color once.
                obj_cmap[idx] += int(one_hot[idx, jdx])*color

    return obj_cmap

# We can use this to plot right ascension and declination.
def plot_celestial_coordinates(patch_of_sky, labels, obj_size = 100, obj_alpha = 1, one_hot = None, obj_cmap = None):

    '''
        patch_of_sky -> the dataframe from SDSS that contains coordinates.
        labels -> the identifiers of the objects.
        obj_size -> the size of the objects for the plot.
        obj_alpha -> the transparency of the objects.
        one_hot -> the one-hot encoding of the objects.
        obj_cmap -> the colors and sizes for the object.
    '''

    # Get the celestial coordinates.
    ra = np.array(patch_of_sky['ra'])
    dec = np.array(patch_of_sky['dec'])
    
    # Adjust the aspect to more reflect the patch of sky.
    dec0 = dec.min()
    dec1 = dec.max()
    
    # Create the figure object.
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect = 1/np.cos((dec0 + dec1)/2*np.pi/180))

    # Checking to see if the object's colormapping is defined.
    if obj_cmap is None:
        ax.scatter(ra, dec, alpha = obj_alpha, s = obj_size, c = 'gold')

    else:
        # If we have the one-hot, then we can use it to label the objects.
        if one_hot is not None:
            for idx in range(one_hot.shape[1]):
                locs = one_hot[:, idx]
                
                ax.scatter(ra[locs], dec[locs], 
                           alpha = obj_alpha, s = obj_size, c = obj_cmap[locs], label = labels[idx])

            ax.legend(loc = 'upper right', bbox_to_anchor = [1.35, 1], frameon = False, fontsize = 12)

        # Otherwise, just plot it without labels or distinction.
        else:
            ax.scatter(ra, dec, alpha = obj_alpha, s = obj_size, c = obj_cmap)


    # Labeling the axes and giving it a title.
    ax.set_ylabel('declination, degrees', fontsize = 12)
    ax.set_xlabel('right ascension, degrees', fontsize = 12)
    ax.set_title('celestial coordinates of the patch', fontsize = 14)

    return fig, ax


def plot_red_shift(patch_of_sky, labels, one_hot = None, obj_cmap = None):

    '''
        patch_of_sky -> the dataframe from SDSS that contains coordinates.
        labels -> the identifiers of the objects.
        one_hot -> the one-hot encoding of the objects.
        obj_cmap -> the colors and sizes for the object.
    '''

    # Get the red shift.
    redshift = patch_of_sky['redshift']

    # Create the figure object.
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Checking to see if the object's colormapping is defined.
    if obj_cmap is None:
        ax.hist(redshift, bins = int(np.sqrt(redshift.shape[0])), color = 'red')

    else:
        # If we have the one-hot, then we can use it to label the objects.
        if one_hot is not None:
            for idx in range(one_hot.shape[1]):
                locs = one_hot[:, idx]
                
                ax.hist(redshift[locs], bins = int(np.sqrt(redshift.shape[0])), 
                        color = obj_cmap[locs][0], label = labels[idx])

            ax.legend(loc = 'upper right', frameon = False, fontsize = 12)

        else:
            print('We need the one-hot in order to proceed.')


    # Labeling the axes and giving it a title.
    ax.set_ylabel('counts', fontsize = 12)
    ax.set_xlabel('red shift relative to the sun', fontsize = 12)
    ax.set_title('red shift of the patch', fontsize = 14)

    return fig, ax