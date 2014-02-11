# Determine the nearest point on a line for a set of points
#
# input:  
#  output_dir:  where result files will be placed
#  point_csv_file:  csv of points (with Longitude, Latitude columns) 
#  line_shape_file:  shapefile of lines
# 
# output (will all be placed in output_dir): 
#  points_on_line.csv:  for each point in point_csv_file, the closest point to
#                       a line in line_shape_file
#  points_distances.csv:  point_csv_file with additional "distance" field
#                         representing the distance to the nearest line in
#                         line_shape_file
#  shortest_lines.shp:  shapefile representing shortest lines from input point
#                       to closest point on a line in line_shape_file
# 
# Run via command line:
# Rscript --vanilla point_to_segment_dists.R output_dir point_csv_file line_shape_file

library(tools)
library(rgdal)
library(geosphere) # must be v1.3-8 or greater

args <- commandArgs(trailingOnly = TRUE)

output_dir_name <- args[1]
input_point_csv_name <- args[2]
input_line_shapefile_name <- args[3]
# 
# input_point_csv_name <- "tmp/demographicsLL.csv"
# input_line_shapefile_name <- "tmp/LeonaNetworks.shp"

# make points a SpatialPointsDataFrame
lonlat <- CRS("+proj=longlat +datum=WGS84")
point_df <- read.csv(input_point_csv_name)
coordinates(point_df) <- ~Longitude+Latitude
proj4string(point_df) <- lonlat

# make network a SpatialLinesDataFrame
shape_dir <- dirname(input_line_shapefile_name)
shape_base <- file_path_sans_ext(basename(input_line_shapefile_name))

# use readOGR b/c it captures the projection
net_df <- readOGR(shape_dir, shape_base)
net_df <- spTransform(net_df, lonlat)

# calculate the dists to lines
dists <- dist2Line(point_df, net_df)
dists_df <- as.data.frame(dists)
# add the distance to the original point dataset
point_df$distance <- dists_df$distance

# create lines representing shortest distance to network
from_mat <- as.matrix(coordinates(point_df))
to_mat <- as.matrix(dists_df[,c("lon", "lat")])
sp_lines_list <- lapply(1:nrow(from_mat), function(i) {
                    Lines(Line(rbind(from_mat[i,], to_mat[i,])),i)
                   })

sp_lines <- SpatialLines(sp_lines_list, lonlat)
lines_data <- data.frame(distance=dists_df$distance, 
                         line_id=dists_df$ID)
sp_lines_df <- SpatialLinesDataFrame(sp_lines, lines_data)

writeOGR(sp_lines_df, output_dir_name, "shortest_lines", "ESRI Shapefile")
write.csv(dists_df, file.path(output_dir_name, "points_on_line.csv"))
write.csv(point_df, file.path(output_dir_name, "points_distances.csv"))
