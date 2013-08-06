# takes args:  output_file csv_filenames
# Run via command line:
# R --no-restore --no-save --args my_map.png sample_1.csv sample_2.csv

args <- commandArgs(trailingOnly = TRUE)

# import required map/plot libs
library(rgdal)
library(ggplot2)
library(maptools)

gpclibPermit()

output_file <- args[1]

input_files <- args[2:length(args)]

# instantiate ggplot
p <- ggplot()
colors <- c("black", "red", "blue", "green", "orange")
min_x <- Inf
max_x <- -Inf
min_y <- Inf
max_y <- -Inf

# merge each point dataset
master <- data.frame(lat=double(0), lon=double(0), group=integer(0))
for (i in 1:length(input_files)) {
    csv_file <- input_files[i]
    df <- read.csv(csv_file, header=TRUE)
    master <- rbind(master, data.frame(lat=df$lat, lon=df$lon, group=rep(i, nrow(df))))
    min_x <- min(df$lon, min_x)
    max_x <- max(df$lon, max_x)
    min_y <- min(df$lat, min_y)
    max_y <- max(df$lat, max_y)
}

# add the master dataframe to the plot
p <- p + geom_point(data=master, aes(x=lon, y=lat, colour=factor(group)))
# project and clip to a sub-region
# coord_map uses mapproj to project
p <- p + coord_map(xlim=c(min_x, max_x), ylim=c(min_y, max_y))

# save it
ggsave(plot=p, filename=output_file)
