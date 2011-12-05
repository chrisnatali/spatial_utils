import rpy2
import numpy
import rpy2.robjects.numpy2ri

#activate r to numpy array auto-conversion
rpy2.robjects.numpy2ri.activate()

to_x = numpy.random.rand(10000) * 100
to_y = numpy.random.rand(10000) * 100

xy = zip(to_x, to_y)

xy_array = numpy.array(xy)

km = rpy2.robjects.r.kmeans(xy_array, 8, 100, 1, "Forgy")

cluster_mapping = numpy.array(km.rx2('clusters'))
cluster_points = numpy.array(km.rx2('centers'))



