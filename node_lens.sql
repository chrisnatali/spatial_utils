-- Query to select nodes and associated line length via 
-- "half length of segment attributed to each connecting node"
-- method. 
-- Assumes nodes and nwk_p (the network) tables in a postgis 2.0
-- enabled DB.
-- (Note the use of ST_GeogFromWKB.  This tells ST_Length to use 
-- spherical distance)
SELECT 
  nodes.cartodb_id, 
  nodes.fid, 
  nodes.the_geom, 
  node_net_len.num_conns, 
  node_net_len.half_len 
FROM
  (SELECT 
     nodes.cartodb_id, 
     SUM(ST_Length(ST_GeogFromWKB(nwk_p.the_geom))/2) half_len, 
     COUNT(nwk_p.cartodb_id) num_conns 
   FROM nwk_p, nodes 
   WHERE ST_INTERSECTS(nodes.the_geom, nwk_p.the_geom) 
   GROUP BY nodes.cartodb_id) node_net_len, 
nodes
WHERE node_net_len.cartodb_id=nodes.cartodb_id;
