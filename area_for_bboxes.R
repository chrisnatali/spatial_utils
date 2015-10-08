#!/usr/bin/env Rscript
# script to calculate geo-spherical surface areas for bounding boxes
# bounding boxes passed in as csv via stdin
# 
# input row format:
# minlon,minlat,maxlon,maxlat
#
# example run
# ```
# ./area_for_bboxes.R <<EOF 2> /dev/null
# > 3.8,7.3,4,7.5
# > 3.81,7.31,4,7.5
# > 3.82,7.32,4,7.5
# > 3.83,7.33,4,7.5
# > EOF
# 488370765
# 440749729
# 395571547
# 352836138

library(geosphere)
bbox_matrix <- as.matrix(read.csv("stdin", header=FALSE))
areas <- apply(bbox_matrix, 1, function(v) { 
    areaPolygon(rbind(c(v[1], v[2]), c(v[3], v[2]), c(v[3], v[4]), c(v[1], v[4]), c(v[1], v[2]))) 
})

cat(areas, sep="\n")
