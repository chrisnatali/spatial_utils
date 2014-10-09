import numpy as np
import math
from itertools import tee, izip

def deg_to_rad(deg):
    return deg * math.pi / 180.0  

EARTH_RADIUS = 6371010

def spherical_distance_vicenty(lon1, lat1, lon2, lat2):
    """
    http://en.wikipedia.org/wiki/Great-circle_distance
    """
    # Convert deg to radians
    lon1_rad = deg_to_rad(lon1)
    lat1_rad = deg_to_rad(lat1)
    lon2_rad = deg_to_rad(lon2)
    lat2_rad = deg_to_rad(lat2)
    
    # only need lon delta
    lon_delta  = lon2_rad - lon1_rad
    # get opposite side unit circle length for angle between points
    y = math.sqrt(math.pow(math.cos(lat2_rad) * math.sin(lon_delta), 2) + 
                  math.pow(math.cos(lat1_rad) * math.sin(lat2_rad) - 
                           math.sin(lat1_rad) * math.cos(lat2_rad) * 
                           math.cos(lon_delta), 2))
                           
    # get adjacent side unit circle length for angle between points
    x = math.sin(lat1_rad) * math.sin(lat2_rad) + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon_delta)

    print "y %s x %s" % (y, x)
    angle = math.atan2(y, x)
    print "angle: %s" % angle
    return EARTH_RADIUS * angle
    

def spherical_distance_haversine(lon1, lat1, lon2, lat2):
    """
    http://en.wikipedia.org/wiki/Great-circle_distance
    """
    # Convert deg to radians
    lon1_rad = deg_to_rad(lon1)
    lat1_rad = deg_to_rad(lat1)
    lon2_rad = deg_to_rad(lon2)
    lat2_rad = deg_to_rad(lat2)
    lon_delta = lon1_rad - lon2_rad
    lat_delta = lat1_rad - lat2_rad
    # Next two lines is the Haversine formula
    inverse_angle = (np.sin(lat_delta / 2) ** 2 + np.cos(lat2_rad) *
                     np.cos(lat1_rad) * np.sin(lon_delta / 2) ** 2)
    haversine_angle = 2 * np.arcsin(np.sqrt(inverse_angle))
    print "angle: %s" % haversine_angle
    return haversine_angle * EARTH_RADIUS

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def linestring_distances(linestring, dist_fun="v"):

    point_arrays = np.transpose(linestring.xy)

    def dist_by_pt_arrays(p0, p1):
        print "p0 %s" % p0
        print "p1 %s" % p1
        if(dist_fun == "h"):
            return spherical_distance_haversine(p0[0], p0[1], p1[0], p1[1])
        else:
            return spherical_distance_vicenty(p0[0], p0[1], p1[0], p1[1])

    return [dist_by_pt_arrays(p0, p1) for p0, p1 in pairwise(point_arrays)]
