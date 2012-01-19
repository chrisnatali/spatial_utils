# sample R code for typical spatial ops

# load the sp spatial library
library('sp')

# generate x, y vectors
x = runif(10, 0.0, 1.0) 
y = runif(10, 0.0, 1.0) 

# create a matrix of them
xy_mat = matrix(c(x, y), ncols=2)

# calculate pairwise distance matrix
# distances are in km and calculated via great circle dist calc
pw_dists = spDists(xy_mat)

# calculate dist to a single point
dists_to_pt = spDistsN1(xy_mat, c(0, 0))
