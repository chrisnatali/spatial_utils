from shapely.wkb import loads
from next.models import Edge
from util import compute_spherical_distance


def generate_nearest_neighbor(scenario, pop_nodes, facility_nodes):
    """
    TODO, look to make this an interface
    Note that this function does not commit any edges to the database.
    arguments:
          scenario: the scenario we are running in
          pop_nodes: an iterable of next.models.Node
          facility_nodes: iterable of next.models.Node

    return: A list of edges that have the property of being a
            relation between a pop_node and its closest facility_node
    """
    edges = []
    for pop_node in pop_nodes:
        nearestDist = ()
        pop_geometry = loads(str(pop_node.point.geom_wkb))
        for fac_node in facility_nodes:
            fac_geometry = loads(str(fac_node.point.geom_wkb))
            between = compute_spherical_distance(pop_geometry.coords[0], fac_geometry.coords[0])
            if between <= nearestDist:
                nearest = fac_node
                nearestDist = between

        edge = Edge(
            scenario,
            pop_node,
            nearest,
            nearestDist)

        edges.append(edge)

    return edges




# Possible ideas for a more abstract process system
# class GeoProcess(object):
#     """
#     """

#     def __init__(self, node_set1, node_set2 ):
#         self.node_set1 = node_set1
#         self.node_set2 = node_set2

#     def __call__(self):
#         raise NameError('You must override this')


# class NN(GeoProcess):

#     def __init__(self, node_set1, node_set2):
#         GeoProcess.__init__(self, node_set1, node_set2)

#     def __call__(self):
#         pass


# nn = NN(pop_node, fac_node)
# nn()
