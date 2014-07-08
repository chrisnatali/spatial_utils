# Render shapefile and rectangle bounds in ggplot
library(maptools) # for loading shapefiles
library(ggplot2)

# load rtrees 
# This one was constructed via iterating and inserting
rtree_iter_leaves <- read.csv("rtree_iter_leaves.out", header=F)
names(rtree_iter_leaves) <- c("id", "num_segments", "ll_lon", "ll_lat", "ur_lon", "ur_lat")

# This one was constructed via an "all at once" approach (should be more efficient)
rtree_leaves <- read.csv("rtree_leaves.out", header=F)
names(rtree_leaves) <- c("id", "num_segments", "ll_lon", "ll_lat", "ur_lon", "ur_lat")

# load network
network <- fortify(readShapeLines("networks-existing.shp"))

# load demand nodes
nodes <- read.csv("demographics.csv")

# plot rtree boundaries (with transparent fill) and the network on top
ggplot() + geom_rect(data=rtree_leaves, aes(xmax=ur_lon, xmin=ll_lon, ymax=ur_lat, ymin=ll_lat), colour="#AF0000", fill="transparent") + geom_line(data=network, aes(x=long, y=lat, group=group), colour="#0000AF")

# needed to display plot
dev.off()

