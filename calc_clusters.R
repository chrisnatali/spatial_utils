# read in dataframe
g_hh = read.table('GS_MV3_Demo_2012_03_02_dropped_HHname.csv', sep=",", header=TRUE)

# extract gps points
xyza = strsplit(as.character(g_hh$gps), split=" ")
xyz_mat = do.call(rbind, xyza)
xyz_df <- data.frame(matrix(as.double(xyz_mat), ncol=4))
colnames(xyz_df) <- c("lat", "lon", "z", "acc")


# put them into a pts matrix
tmp = c(xyz_df$lat, xyz_df$lon)
pts = matrix(tmp, ncol=2)

# calc dists
sp_dists <- spDists(pts, longlat=TRUE)
dists <- as.dist(sp_dists)

# cluster
tree <- hclust(dists, method="average")
clusts = cutree(tree, h=1.0)  #** Change h value to vary cluster distance

# accumulate cluster pts, hh_members
for (i in min(clusts):max(clusts)) lst_clsts[[i]] <- matrix(nrow=0, ncol=3)
for (j in 1:length(clusts)) {
    lst_clsts[[clusts[j]]] <- rbind(lst_clsts[[clusts[j]]], c(pts[j,], g_hh$hh_members[j]))
}

# create df for results
res_df <- data.frame(lat=double(0), lon=double(0), pop=numeric(0), mid=double(0))

# calculate center pts, sum hh's, mean interhousehold distance
for (k in 1:length(lst_clsts)) {
  cluster <- lst_clsts[[k]]
  lat <- mean(cluster[,1])
  lon <- mean(cluster[,2])
  pop  <- sum(cluster[,3])
  cluster_pts <- matrix(c(cluster[,1], cluster[,2]), ncol=2)
  cluster_sp_dists <- spDists(cluster_pts, longlat=TRUE)
  cluster_dists <- as.dist(cluster_sp_dists)
  mid <- mean(cluster_dists) * 1000
  res_df <- rbind(res_df, data.frame(lat=lat, lon=lon, pop=pop, mid=mid))
}

# TODO:  Find out where NA's are coming from

# Write out file
write.table(res_df, file="ghana_hh_cluster.csv", sep=",", row.names=FALSE)
  
