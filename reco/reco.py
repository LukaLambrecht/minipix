import numpy as np


def max_diameter( cluster, method='full' ):
    ### determine the maximum diameter of a cluster of points
    # help function for cluster_type (see below)
    # input arguments:
    # - cluster: list representing a point cluster;
    #   each element in the list is a tuple with point coordinates
    
    if method=='full':
        # calculate distances between all points and get maximum
        dists = []
        for idx,point1 in enumerate(cluster):
            for point2 in cluster[idx+1:]:
                dist = (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2
                dist = np.sqrt(dist)
                dists.append(dist)
        dists = np.array(dists)
        maxdist = np.amax(dists)
        return maxdist
    else:
        msg = 'ERROR in reco.py / max_diameter:'
        msg += 'method "{}" not recognized.'.format(method)
        raise Exception(msg)
        
def center( cluster, method='full' ):
    ### get the center of a cluster
    # input arguments:
    # - cluster: list representing a point cluster;
    #   each element in the list is a tuple with point coordinates
    
    if method=='full':
        # calculate (squared) distances from each point to all other points
        # and take the point for which the sum is minimal
        idx = 0
        minsumdists = 1e6
        for i,point1 in enumerate(cluster):
            sumdists = 0
            for point2 in cluster:
                dist = (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2
                sumdists += dist
            if sumdists < minsumdists:
                minsumdists = sumdists
                idx = i
        return cluster[idx]
    else:
        msg = 'ERROR in reco.py / center:'
        msg += 'method "{}" not recognized.'.format(method)
        raise Exception(msg)

def cluster_type( cluster ):
    ### get the type of a cluster
    # input arguments:
    # - cluster: list representing a point cluster;
    #   each element in the list is a tuple with point coordinates
    # returns:
    #   a string representing the cluster type;
    #   see below for options and definitions.
    
    if len(cluster)==1:
        return 'dot'
    maxd = max_diameter(cluster)
    if maxd>4: return 'line'
    else: return 'blob'