import numpy as np
import math


def overlap_circle_square( R, center, size ):
    ### calculate the overlap between a cirlce and a square
    # input arguments:
    # - R: radius of the circle, assumed to be centered on the origin.
    # - center: tuple of (x,y), center point of the square, 
    # - size: length of the side of the square.
    # returns: fraction of square area overlapping with circle
    # todo: find analytical expression
    # for now: approximate using smaller squares
    noverlap = 0
    ndiv = 20
    for x in np.linspace(center[0]-size/2, center[0]+size/2, num=ndiv):
        for y in np.linspace(center[1]-size/2, center[1]+size/2, num=ndiv):
            if np.sqrt(x**2+y**2)<R: noverlap += 1
    foverlap = noverlap/ndiv**2
    return foverlap

def generate_blob( npixels ):
    ### generate arbitrarily sized blobs of approximately circular shape
    # input parameters:
    # - npixels: size of the blob in number of pixels
    #            if npixels is 1: return a single pixel
    #            if npixels is 2: return randomly oriented two-pixel cluster
    #            if npixels is > 2: an approximate circle is generated
    #            (note that the actual number of pixels is probabilistic 
    #             and can deviate from npixels in this case)
    rng = np.random.default_rng()
    if npixels==1:
        return [(0,0)]
    elif npixels==2:
        rn = rng.uniform()
        if( rn<0.25 ): return [(0,0), (0,1)]
        elif( rn>0.25 and rn<0.5 ): return [(0,0), (0,-1)]
        elif( rn>0.5 and rn<0.75 ): return [(0,0), (1,0)]
        else: return [(0,0), (-1,0)]
    else:
        res = []
        # find radius of approximating circle
        r = math.sqrt(npixels/math.pi)
        # find half-size of enclosing rectangle
        sqs = int(math.ceil(r))
        # loop over candidate pixels
        for i in range(-sqs,sqs):
            for j in range(-sqs,sqs):
                # calculate overlap of pixel with approximating circle
                foverlap = overlap_circle_square(r, (i,j), 1)
                # add this pixel with a given probability
                if rng.uniform()<foverlap: res.append((i,j))
        return res
    
def generate_line( npixels ):
    ### generate a straight line with random orientation
    # input arguments:
    # - npixels: size of the line in number of pixels
    #            (note that the actual number of pixels can deviate from npixels)
    rng = np.random.default_rng()
    # generate random angle
    theta = rng.uniform()*2*math.pi
    # calculate ending point of the line
    xend = npixels*np.cos(theta)
    yend = npixels*np.sin(theta)
    # travel along the line and add all pixels
    res = [(0,0)]
    nsteps = npixels*20
    for t in range(nsteps):
        x = t/nsteps*xend
        y = t/nsteps*yend
        xcoord = int(round(x))
        ycoord = int(round(y))
        if res[-1]!=(xcoord,ycoord):
            res.append((xcoord,ycoord))
    return res       