library(rgdal)
library(ggplot2)
library(maptools)

gpclibPermit()

# get the network data
net.map <- readOGR(dsn="PG:dbname=gis_test", layer="net_230")

# and the node data with segment connections attribute
node.map <- readOGR(dsn="PG:dbname=gis_test", layer="node_lens_230")

# setup the network data as a dataframe like ggplot likes it
net.ggmap <- fortify(net.map)

# setup a node dataframe for ggplot
node.df <- data.frame(coordinates(node.map)[,1:2], num_conns = node.map$num_conns, net_len = node.map$net_len)

# instantiate ggplot
p <- ggplot()
# add the network
my.map <- p + geom_line(data=net.ggmap, aes(x=long, y=lat, group=group)) 
# add the node
my.map <- my.map + geom_point(data=node.df, aes(x=coords.x1, y=coords.x2, color = factor(num_conns))) 
# project and clip to a sub-region
my.map <- my.map + coord_map(xlim=c(120.5, 120.75), ylim=c(-8.75, -8.5))

# save it
ggsave(plot=my.map, filename="np_net_conns.png")

