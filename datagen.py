import numpy as np


def generate_object( size ):
    ### generate a single object (i.e. a few neighbouring pixels set to 1)
    # note: mostly for internal use!
    # input arguments:
    # - size: number of pixels to set to 1
    # returns:
    #   a list of coordinate tuples to set to 1
    # note: for now only simple shapes are implemented; to be extended.
    # note: the returned coordinates are always centered around (0,0),
    #       i.e. only the shape is generated (not the position);
    #       additional processing should be done to place the object 
    #       somewhere in an image.
    rng = np.random.default_rng()
    if size==1:
        return [(0,0)]
    elif size==2:
        if rng.uniform()<0.5: return [(0,0), (0,1)]
        else: return [(0,0), (1,0)]
    else:
        raise Exception('ERROR in datagen.py / generate_object:'
                        +' size {} not yet supported'.format(size))
    
def generate_position( image_size ):
    ### generate a single random position in an image
    # note: mostly for internal use!
    # input arguments:
    # - image_size: tuple of height and width in pixels
    # returns:
    #   a tuple of coordinates
    rng = np.random.default_rng()
    xcoord = int(rng.uniform()*image_size[0])
    ycoord = int(rng.uniform()*image_size[1])
    return (xcoord,ycoord)

def position_object( obj, position, image_size ):
    ### modify the coordinates of a generated object to fit in an image
    # note: mostly for internal use!
    # input arguments:
    # - obj: a list of coordinate tuples centered around (0,0)
    #        (e.g. the result of generate_object)
    # - position: a tuple of coordinates
    #             (e.g. the result of generate_position)
    # - image_size: a tuple of height and width of the image,
    #               used for removing out-of-bounds coordinates
    # returns:
    #   a new object with translated coordinates
    newobj = []
    for coords in obj:
        newxcoord = coords[0]+position[0]
        newycoord = coords[1]+position[1]
        if( newxcoord<0 or newxcoord>=image_size[0]
            or newycoord<0 or newycoord>=image_size[1] ): continue
        newobj.append((newxcoord, newycoord))
    return newobj
    
def generate_image( image_size=(256,256), 
                    objects={1:1} ):
    ### generate a single image
    # input arguments:
    # - image_size: tuple of height and width in pixels
    # - objects: a dictionary with the number of objects per object size in pixels
    # returns:
    #   a numpy array of shape image_size
    im = np.zeros(image_size)
    for objsize in objects.keys():
        for objn in range(objects[objsize]):
            # get an object shape and position
            obj = generate_object(objsize)
            objpos = generate_position(image_size)
            obj = position_object( obj, objpos, image_size )
            # add the object to the image
            for coord in obj:
                im[coord[0],coord[1]] = 1
    return im