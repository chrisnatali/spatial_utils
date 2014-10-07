CREATE TABLE node_lens AS
SELECT
  nodes.gid, 
  nodes.fid, 
  nodes.geom, 
  node_net_len.num_conns, 
  node_net_len.half_len 
FROM
  (SELECT 
    nodes.gid, 
    sum(ST_Length(ST_GeogFromWKB(net.geom))/2) half_len, 
    count(net.gid) num_conns 
   FROM net, nodes 
   WHERE 
     st_intersects(nodes.geom, net.geom) 
   GROUP BY nodes.gid) node_net_len, 
  nodes 
WHERE 
  node_net_len.gid=nodes.gid;
