my_g_plot <- function(g, id, transform=FALSE, vert_label="name", edge_label="name", width=1000, height=1000, vertex.size=4) {
    # get coords in mercator proj
   v.labels <- get.vertex.attribute(g, vert_label)
   e.labels <- get.edge.attribute(g, edge_label)
   png(paste("plots/plot", id, ".png", sep=""), 
        type="cairo-png", 
        width=width, height=height)
    if(transform) {
        vec_df <- get.data.frame(g, what="vertices")
        xy <- vec_df[,c("X", "Y")]
        coordinates(xy) <- ~X+Y
        proj4string(xy) <- CRS("+proj=longlat +ellps=WGS84")
        xy <- spTransform(xy, CRS("+proj=merc +ellps=WGS84"))
        plot(g, layout=xy@coords, vertex.size=vertex.size, edge.arrow.size=1, vertex.label=v.labels, edge.label=e.labels)
    } else {
        plot(g, vertex.size=vertex.size, edge.arrow.size=1, vertex.label=v.labels, edge.label=e.labels)
    }
    dev.off()
}

# sample networkplanner.R usage (assumes it's installed)
library(networkplanner)
 
# loop through scenarios creating
scen_id_file <- "~/np_data/sids"
scenario_dirs <- read.csv(scen_id_file)[,1]
scenario_dirs <- c("2970", "2972", "2971", "2973", "2974")
scenario_dirs <- c("2940")
scenario_dirs <- paste("~/np_data", scenario_dirs, sep="/")

for (scenario_dir in scenario_dirs) {
    # select scenario dir (assumes available on system)
    # read into a NetworkPlan
    np <- read_networkplan(scenario_dir)
    # accumulate and sequence it
    np <- sequence_plan_far(np, sequence_model=mv_v_dmd_sequence_model) 
    # write it
    write.NetworkPlan(np, scenario_dir)
}

df_to_list <- function(df) { 
    l <- list()
    for(rname in row.names(df)) {
        l[[rname]] <- list()
        for(name in names(df)) {
            l[[rname]][[name]] <- df[rname, name]
        }
    }
    l
}

list_of_lists_to_df <- function(l_o_l) { 
    col_attrs <- t(sapply(l_o_l, names))
    col_names <- Reduce(union, col_attrs)
    stopifnot(ncol(col_attrs)==length(col_names)) 
    res_df <- as.data.frame(sapply(col_names, 
                function(nm) { Reduce(c, 
                    sapply(l_o_l, function(l) { 
                        ifelse(is.null(l[nm][[1]]), NA, l[nm]) }))
                }))
    names(res_df) <- col_names
    res_df
}  

# must conform to networkplanner.R format
json_to_igraph <- function(json_str) {
    js_list <- fromJSON(json_str)
    vdf <- list_of_lists_to_df(js_list$vertices)
    vdf$id <- 1:nrow(vdf)
    col_names <- setdiff(names(vdf), "id")
    col_names <- c("id", col_names)
    vdf <- vdf[,col_names]
    edf <- list_of_lists_to_df(js_list$edges)
    graph.data.frame(edf, FALSE, vdf)
} 
       
#TODO
igraph_to_json <- function(ig) {
    vdf <- get.data.frame(ig, what="vertices") 
    edf <- get.data.frame(ig, what="edges") 
    l <- list()
    l$vertices <- df_to_list(vdf)   
    l$edges <- df_to_list(edf)   

    l
}
