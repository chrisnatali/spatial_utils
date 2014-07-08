# Simple script to count number of segments in a shapefile
library(maptools)

args <- commandArgs(TRUE)

if (length(args) > 0) {
  shapefile = args[1]
  network <- readShapeLines(shapefile)
  coord_lens <- lapply(lapply(lapply(lapply(network@lines, slot, name="Lines"), "[[", 1), slot, name="coords"), nrow)
  coord_lens <- as.numeric(coord_lens)
  print(length(coord_lens))
  print(mean(coord_lens))
}
