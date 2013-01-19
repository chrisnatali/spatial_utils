select nodes.cartodb_id, nodes.fid, nodes.the_geom, nodes.the_geom_webmercator, node_net_len.num_conns from
(SELECT nodes.cartodb_id, sum(ST_Length(ST_GeogFromWKB(nwk_p.the_geom))/2) half_len, count(nwk_p.cartodb_id) num_conns FROM nwk_p, nodes where st_intersects(nodes.the_geom, nwk_p.the_geom) group by nodes.cartodb_id) node_net_len, nodes where node_net_len.cartodb_id=nodes.cartodb_id;
