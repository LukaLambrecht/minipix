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
        print(coord)
        for testcoord in coords[:i]:
            if( abs(coord[0]-testcoord[0])<2 and abs(coord[1]-testcoord[1])<2 ):
                valid = False
                print('reject')
                break
        if valid: newcoords.append(coord)
    return newcoords

def count_objects_cluster( image ):
    ### object counting method using proximity clusters
    # method: essentially equal to count_objects_simple,
    #         but more clever way of removing double counting
    coords = count_objects_pixels(image)
    clusters = []
    unclustered = [True]*len(coords)
    for i in range(len(coords)):
        # check if point already belongs to a cluster
        if( not unclustered[i] ): continue
        # initiate the cluster with this point
        cluster = [i]
        unclustered[i] = False
        addedpoints = 1
        # keep adding points to the cluster until no close points are left
        while addedpoints>0:
            addedpoints = 0
            # loop over currently unclustered points
            unclustered_inds = [k for k in range(len(coords)) if unclustered[k]]
            for j in unclustered_inds:
                testcoord = coords[j]
                # loop over all points in current cluster
                for k in cluster:
                    testcoord2 = coords[k]
                    # test distance
                    if( abs(testcoord[0]-testcoord2[0])<2 and abs(testcoord[1]-testcoord2[1])<2 ):
                        cluster.append(j)
                        unclustered[j] = False
                        addedpoints += 1
                        break
        # add the cluster for this point
        clusters.append(cluster)
    # format the result as the coordinates of the first point in each cluster
    res = []
    for cluster in clusters: res.append(coords[cluster[0]])
    return res