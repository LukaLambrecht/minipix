import numpy as np
import importlib
import objectgen
importlib.reload(objectgen)


def generate_object( size, shape='blob' ):
    ### generate a single object (i.e. a few neighbouring pixels set to 1)
    # note: mostly for internal use!
    # input arguments:
    # - size: size of the object in number of pixels
    # - shape: choose from 'blob', 'line'
    # returns:
    #   a list of coordinate tuples
    # note: for now only simple shapes are implemented; to be extended.
    # note: the returned coordinates are always centered around (0,0),
    #       i.e. only the shape is generated (not the position);
    #       additional processing should be done to place the object 
    #       somewhere in an image.
    if shape=='blob':
        return objectgen.generate_blob( size )
    elif shape=='line':
        return objectgen.generate_line( size )
    else:
        raise Exception('ERROR in datagen.py / generate_object:'
                        +' shape {} not recognized.'.format(shape))
    
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
                    objects={'blob':{1:1}} ):
    ### generate a single image
    # input arguments:
    # - image_size: tuple of height and width in pixels
    # - objects: a dictionary with the properties of the objects to generate,
    #            e.g. {'blob':{1:2},'line':{4,1}} will result in 
    #            2 instance of a size 1 blob and 1 instance of a size 4 line.
    # returns:
    #   a numpy array of shape image_size
    im = np.zeros(image_size)
    for objshape in objects.keys():
        thisobjects = objects[objshape]
        for objsize in thisobjects.keys():
            for objn in range(thisobjects[objsize]):
                # get an object shape and position
                obj = generate_object(objsize,shape=objshape)
                objpos = generate_position(image_size)
                obj = position_object( obj, objpos, image_size )
                # add the object to the image
                for coord in obj:
                    im[coord[0],coord[1]] = 1
    return im