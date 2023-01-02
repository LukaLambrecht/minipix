import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def reco_plot(image, figsize=(12,12), cmap='gray',
              objects=None, cdict=None, ldict=None, boxhalfwidth=5):
    ### make a plot of an image with reconstructed object coordinates.
    # the result is a black-and-white image as detected (or generated)
    # with coloured squares centered on the coordinates of reconstructed objects.
    # input arguments:
    # - image: 2D numpy array representing the image
    # - figsize: size of the resulting plot
    # - cmap: colormap of the underlying image
    # - objects: list of dictionaries holding object parameters;
    #   each dictionary should have the following form:
    #   {'coords': (<row coordinate>, <column coordinate>), 'type': <some type identifier string>}
    #   e.g.: {'coords': (16,25), 'type':'line'}
    # - cdict: dictionary matching object types to matplotlib colors,
    #   e.g.: {'line': 'blue'}
    # - ldict: dictionary matching object types to labels for the legend,
    #   e.g.: {'line': 'Lines'}
    # - boxhalfwidth: half width of each square (in image pixels)
    # returns:
    # a tuple with the figure and axes
    
    # make the figure
    fig,ax = plt.subplots( figsize=figsize )
    # plot the image
    ax.imshow( image, cmap=cmap )
    if objects is None: return (fig,ax)
    # plot a colored square for each object
    labels = []
    for obj in objects:
        if not isinstance(obj, dict):
            msg = 'ERROR in plotting.py / reco_plot:'
            msg += ' object is of type {}'.format(type(obj))
            msg += ' while a dict was expected.'
            raise Exception(msg)
        if not 'coords' in obj.keys():
            msg = 'ERROR in plotting.py / reco_plot:'
            msg += ' object does not contain required key "coords".'
            raise Exception(msg)
        patchxcoord = obj['coords'][1]
        patchycoord = obj['coords'][0]
        color = 'r'
        label = 'Reco'
        if 'type' in obj.keys():
            otype = obj['type']
            if cdict is not None: color = cdict[otype]
            if ldict is not None: label = ldict[otype]
        else:
            msg = 'WARNING in plotting.py / reco_plot:'
            msg += ' object does not contain expected key "type",'
            msg += ' will use default settings for color and label.'
            print(msg)
        if label in labels: label = None
        else: labels.append(label)
        anchor = (patchxcoord-boxhalfwidth,patchycoord-boxhalfwidth)
        box = mpl.patches.Rectangle(anchor, 2*boxhalfwidth, 2*boxhalfwidth,
                                    edgecolor=color, facecolor=(0,0,0,0), 
                                    label=label)
        ax.add_patch(box)
    # plot aesthetics
    ax.legend()
    # return the result
    return (fig,ax)

def reco_plot_default(image, objects):
    ### same as reco_plot but with some convenient default settings hard-coded.
    cdict = ({
        'dot': 'r',
        'blob': 'g',
        'line': 'b'
      })
    ldict = ({
        'dot': 'Dot ({})'.format(len([el for el in objects if el['type']=='dot'])),
        'blob': 'Blob ({})'.format(len([el for el in objects if el['type']=='blob'])),
        'line': 'Line ({})'.format(len([el for el in objects if el['type']=='line']))
      })
    boxhalfwidth = int(max(image.shape)/50)
    return reco_plot( image, objects=objects, cdict=cdict, ldict=ldict, 
                      boxhalfwidth=boxhalfwidth )