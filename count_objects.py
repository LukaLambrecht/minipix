import numpy as np


def count_objects_pixels( image ):
    ### simple object counting method
    # method: count pixels that are nonzero.
    # input arguments:
    # - image: 2D numpy array
    # returns:
    #   a list of coordinate tuples
    (xcoords,ycoords) = np.nonzero(image)
    coords = [(xcoord,ycoord) for xcoord,ycoord in zip(xcoords,ycoords)]
    return coords

def count_objects_simple( image ):
    ### simple object counting method
    # method: count pixels that are nonzero and remove double-counting
    #         from neighbouring pixels
    coords = count_objects_pixels(image)
    newcoords = []
    for i,coord in enumerate(coords):
        valid = True
        for testcoord in coords[:i]:
            if( (coord[0]==testcoord[0] and abs(coord[1]-testcoord[1])<2)
                or (coord[1]==testcoord[1] and abs(coord[0]-testcoord[0])<2)):
                valid = False
                break
        if valid: newcoords.append(coord)
    return newcoords