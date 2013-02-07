import pysal.cg
import numpy

x1 = numpy.random.rand(10000)
y1 = numpy.random.rand(10000)

x2 = numpy.random.rand(10000)
y2 = numpy.random.rand(10000)

from_pts = numpy.column_stack((x2, y2))
to_pts = numpy.column_stack((x1, y1))

kd = pysal.cg.Arc_KDTree(from_pts, radius=pysal.cg.RADIUS_EARTH_KM)
d,i = kd.query(to_pts, k=1)
