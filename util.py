import numpy
import csv
import rpy2
from rpy2.robjects import r
import math

def rand_pts(n, scale):
    """ Generate n random x,y points with values from 0-1 scaled by scale value"""
    x = numpy.random.rand(n) * scale
    y = numpy.random.rand(n) * scale
    xy = zip(x, y)
    return xy

def points_to_centroid(pts):
    """ Calculates the centroid of the points.  
    pts:  a 2D numpy array where element 0 is the list of x coords,
    and element 1 is the list of y's.
    returns centroid as an x, y tuple
    """

    #print pts
    if(len(pts) != 2):
        return ()

    x_coords = pts[0]
    y_coords = pts[1]
    centroid_x = sum(x_coords) / len(x_coords)
    centroid_y = sum(y_coords) / len(y_coords)

    return (centroid_x, centroid_y)


def dists_to_pt(pts, pt, use_great_circle=True):
    """ Returns a list of distances (in km) from each of the points to
    to the pt (uses great_circle_distance)
    pts:  """
    rpy2.robjects.numpy2ri.activate()
    np_pts = numpy.array(pts)
    np_pt = numpy.array(pt)
    dists_to_pt = r.spDistsN1(np_pts, np_pt, longlat=use_great_circle)
    return dists_to_pt


def get_bounds(pts):
    """ Returns low-left x, low-left y, up-right x, up-right y """
    np_pts = numpy.array(pts)
    x_pts = np_pts[:, 0]
    y_pts = np_pts[:, 1]
    return [min(x_pts), min(y_pts), max(x_pts), max(y_pts)]


def compute_spherical_distance(pt1, pt2):
    """
    http://en.wikipedia.org/wiki/Great-circle_distance
    """
    # Define
    convertDegreesToRadians = lambda x: x * math.pi / 180
    # Load
    longitude1, latitude1 = map(convertDegreesToRadians, pt1)
    longitude2, latitude2 = map(convertDegreesToRadians, pt2)
    # Initialize
    longitudeDelta = longitude2 - longitude1
    earthRadiusInMeters = 6371010
    # Prepare
    y = math.sqrt(math.pow(math.cos(latitude2) * math.sin(longitudeDelta), 2) + math.pow(math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(longitudeDelta), 2))
    x = math.sin(latitude1) * math.sin(latitude2) + math.cos(latitude1) * math.cos(latitude2) * math.cos(longitudeDelta)
    # Return
    return earthRadiusInMeters * math.atan2(y, x)
