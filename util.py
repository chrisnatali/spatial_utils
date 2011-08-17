from collections import deque

class Bounds:
    """Rectangular bounds, takes 2 tuples representing
       the lower left and upper right of the bounds"""
    def __init__(self, sw, ne):
        self.min_x = sw[0]
        self.min_y = sw[1]
        self.max_x = ne[0]
        self.max_y = ne[1]

    def intersects(self, other):
        return overlaps((self.min_x, self.max_x), \
                        (other.min_x, other.max_x)) and \
               overlaps((self.min_y, self.max_y), \
                        (other.min_y, other.max_y))

    def __str__(self):
        return "sw: {0},{1} ne: {2},{3}".format( \
                self.min_x, self.min_y, self.max_x, self.max_y)

class QuadTree:
    """class representing a point QuadTree with a maximum
       number of points per leaf."""
    def __init__(self, per_leaf, sw, ne):
        self.per_leaf = per_leaf
        self.root = self.QuadNode(sw, ne)

    class QuadNode:
        """node within the QuadTree.  Leaves contain points.
           non-leaves do not."""
        def __init__(self, sw, ne):
            self.bounds = Bounds(sw, ne)
            self.points = []
            self.quads = []
       
        def __str__(self):
            return self.bounds.__str__() + "|" + self.points.__str__()
             
    def __str__(self):
        return self.to_str(self.root)

    def to_str(self, quad_node):
        str = ""
        quad_queue = deque()
        quad_queue.append(quad_node)
        while quad_queue:
            curr_qn = quad_queue.popleft() 
            str += "{0}\n".format(curr_qn.__str__())
            for qn in curr_qn.quads:
                quad_queue.append(qn)
        return str
            
    def divide_quad(self, quad_node):
        """ Split the node into 4 equal sized quadrants
            and return them. """
        bnds = quad_node.bounds
        x_diff = bnds.max_x - bnds.min_x
        y_diff = bnds.max_y - bnds.min_y
        x_dist = x_diff / 2
        y_dist = y_diff / 2
        quad_nodes = []
        ne = self.QuadNode((bnds.min_x + x_dist, bnds.min_y + y_dist), \
                      (bnds.max_x, bnds.max_y))
        se = self.QuadNode((bnds.min_x + x_dist, bnds.min_y), \
                      (bnds.max_x, bnds.min_y + y_dist)) 
        sw = self.QuadNode((bnds.min_x, bnds.min_y), \
                      (bnds.min_x + x_dist, bnds.min_y + y_dist)) 
        nw = self.QuadNode((bnds.min_x, bnds.min_y + y_dist), \
                      (bnds.min_x + x_dist, bnds.max_y)) 
        quad_nodes.append(ne)
        quad_nodes.append(se)
        quad_nodes.append(sw)
        quad_nodes.append(nw)
        return quad_nodes
        
    def add(self, pt):
        """ Add the point to the appropriate node
            in the QuadTree """
        self.add_pt(pt, self.root)

    def add_pt(self, pt, quad_node):
        """ Recursively look for the appropriate
            node to insert the point into.  Create
            new quadrants when existing leaf nodes
            get full. """
        if not quad_node.quads: # this is a leaf
            if len(quad_node.points) < self.per_leaf:
                quad_node.points.append(pt)
                return
            else:
                quad_node.quads = self.divide_quad(quad_node)
                pts = quad_node.points
                pts.append(pt)
                quad_node.points = []
                for qpt in pts:
                    self.add_pt(qpt, quad_node)
        else:
            quad_ind = get_containing_quad(pt, quad_node.quads) 
            self.add_pt(pt, quad_node.quads[quad_ind]) 
            


def get_containing_quad(pt, quads):
   """ return the index of the quadrant containing the point """
   for i in range(len(quads)):
        if contains(pt, quads[i].bounds):
            return i

def contains(pt, bounds):
    """Determine whether the point is within the bounds"""
    return ((bounds.min_x <= pt[0] <= bounds.max_x) and \
            (bounds.min_y <= pt[1] <= bounds.max_y))

def overlaps(r1, r2):
    """Determine whether range r1 overlaps range r2
       range is defined a 2 element tuple where element
       0 is the min and 1 is the max of the range"""
    return (r2[0] <= r1[0] <= r2[1]) or \
           (r1[0] <= r2[0] <= r1[1]) or \
           (r1[0] == r2[1] or r2[0] == r1[1])


 
