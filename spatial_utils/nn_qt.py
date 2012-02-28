import quad_tree 
import util

def generate_nearest_neighbor(pop_pts, fac_pts):
    """
    Nearest Neighbor via QuadTree.  
    Faster than "naive" approach for large number of
    facilities (i.e. > 1000)
    arguments:
          pop_pts: an iterable of x,y pairs 
          fac_pts: iterable of x,y pairs

    return: A list of pop_pt index, fac_pt index, & distance
            representing facilities closest to pop pts & the distance between 
            
    """
    edges = []
    bounds =  util.get_bounds(pop_pts + fac_pts)
    qt = quad_tree.QuadTree(10, bounds[:2], bounds[2:], 
            lambda x: x['pt'], True)

    for n in range(0, len(fac_pts)):
        fac_dict = {'id': n, 'pt': fac_pts[n]}
        qt.add(fac_dict)

    for m in range(0, len(pop_pts)):
        pop_pt = pop_pts[m]
        fac_dict = qt.find_nearest(pop_pt)
        dist = util.compute_spherical_distance(pop_pt, fac_dict['pt'])
        edge = [m, fac_dict['id'], dist]
        edges.append(edge)

    return edges
