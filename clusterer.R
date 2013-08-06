# takes args:  csv_filename cluster_dist(in km) 
# Can be run via the command line with something like:
#  R --no-restore --no-save --args norm_sample.csv 30.0 < clusterer.R

args <- commandArgs(trailingOnly = TRUE)

# import sp library
library(sp)

csv_file = args[1]
cluster_dist = as.double(args[2])
rm(args)

# get the lat/lon matrix from the input csv
# (assumes the file is clean/formatted prior to input)
lat_lon <- read.table(csv_file, sep=",", header=TRUE)
tmp <- c(lat_lon$lat, lat_lon$lon)
pts <- matrix(tmp, ncol=2)

# calculate distances (assumes spherical coordinates)
sp_dists <- spDists(pts, longlat=TRUE)
dists <- as.dist(sp_dists)

# cluster
# calculate the agglomerative cluster tree to a root
tree <- hclust(dists, method="average") 
# clut the tree at a specified "height" (a distance in km)
clusts <- cutree(tree, h=cluster_dist)

# create a 3 col empty matrix for each cluster
cluster_list <- list()
for (i in min(clusts):max(clusts)) cluster_list[[i]] <- matrix(nrow=0, ncol=2)
# group the points in each cluster into its corresponding list element
for (j in 1:length(clusts)) {
    cluster_list[[clusts[j]]] <- rbind(cluster_list[[clusts[j]]], pts[j,])
}

# create df for results
results <- data.frame(lat=double(0), lon=double(0), mid=double(0), count=integer(0))

# itereate over clusters, calculating representative points (their mean) and mean interpoint distance
for (k in 1:length(cluster_list)) {
    cluster <- cluster_list[[k]]
    len <- length(cluster)/2
    lat <- mean(cluster[,1])
    lon <- mean(cluster[,2])
    cluster_pts <- matrix(c(cluster[,1], cluster[,2]), ncol=2)
    cluster_sp_dists <- spDists(cluster_pts, longlat=TRUE)
    cluster_dists <- as.dist(cluster_sp_dists)
    mid <- mean(cluster_dists) * 1000 # for kilometers
    results <- rbind(results, data.frame(lat=lat, lon=lon, mid=mid, count=len))
}

# write to stdout as csv
write.table(results, file="", sep=",", row.names=FALSE)
