import numpy as np
import reco


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
            if( abs(coord[0]-testcoord[0])<2 and abs(coord[1]-testcoord[1])<2 ):
                valid = False
                break
        if valid: newcoords.append(coord)
    return newcoords

def count_objects_cluster( image, returntype='center' ):
    ### object counting method using proximity clusters
    # method: essentially equal to count_objects_simple,
    #         but more clever way of removing double counting
    # returns: depends on returntype argument:
    # - 'first': return list with tuples of first point coordinates (one per cluster).
    #   for each cluster, the first point is returned.
    #   this requires no extra calculation, but the choice of 'first point' is arbitrary
    #   and might depend on the used clustering algorithm.
    # - 'center': return list with tuples of central point coordinates (one per cluster).
    #   for each cluster, the central point is returned.
    #   see reco.py / center for the definition of the central point.
    # - 'full': return list of lists with tuples of cluster point coordinates.
    #   for each cluster, the full list of points is returned.
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
    # format the result
    res = []
    for cluster in clusters:
        if returntype=='first':
            res.append( coords[cluster[0]] )
        elif( returntype=='full' or returntype=='center' ):
            clustercoords = [coords[i] for i in cluster]
            if returntype=='full':
                res.append( clustercoords )
            elif returntype=='center':
                center = reco.center( clustercoords )
                res.append(center)
        else:
            msg = 'ERROR in counting.py / count_objects_cluster:'
            msg += 'returntype "{}" not recognized.'.format(returntype)
            raise Exception(msg)
    return res

def reco_objects( image ):
    ### extension of count_objects_cluster with determination of cluster type
    clusters = count_objects_cluster( image, returntype='full' )
    cinfos = []
    for cluster in clusters:
        center = reco.center(cluster)
        ctype = reco.cluster_type(cluster)
        cinfo = {'coords': center, 'type': ctype}
        cinfos.append(cinfo)
    return cinfos