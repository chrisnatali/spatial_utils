import rpy2
import numpy
from rpy2.robjects import r
import rpy2.robjects.numpy2ri

#activate r to numpy array auto-conversion
rpy2.robjects.numpy2ri.activate()

#load sp library
r.library('sp')

to_x = numpy.random.rand(100) * 100
to_y = numpy.random.rand(100) * 100

xy = zip(to_x, to_y)

xy_array = numpy.array(xy)

dists = r.spDists(xy_array)
tree = r.hclust(r('as.dist')(dists), "average")
clusts = r.cutree(tree, h=100.0)

np_clusts = numpy.array(clusts)

clusters = [[] for i in range(max(np_clusts))]
for i in range(0, len(np_clusts)):
   clusters[np_clusts[i] - 1].append(xy_array[i])

cluster1 = clusters[len(clusters) - 1]
cluster1_cols = numpy.array(cluster1)
print cluster1_cols
print cluster1[0]
dists = r.spDistsN1(cluster1_cols, cluster1[0])
print dists
