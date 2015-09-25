import pandas as pd
import geopandas as gpd
from geopandas.io import osm
from geopandas.tools import sjoin

# network_shp_file = "/home/cjn/np_data/bad_scenario3/networks-proposed.shp"
country_shp_file = "/home/cjn/geodata/ne_10m_admin_0_countries_lakes/ne_10m_admin_0_countries_lakes.shp"

# line_shp = gpd.read_file(network_shp_file)
country_shp = gpd.read_file(country_shp_file)

myanmar = country_shp[country_shp.ADMIN=='Myanmar']
nigeria = country_shp[country_shp.ADMIN=='Nigeria']

osm_places_mmr = osm.query_osm(typ='node', bbox=myanmar.total_bounds, recurse='down', tags='place')
osm_power_mmr = osm.query_osm(typ='node', bbox=myanmar.total_bounds, recurse='down', tags='power')

osm_places_nga = osm.query_osm(typ='node', bbox=nigeria.total_bounds, recurse='down', tags='place')
osm_power_nga = osm.query_osm(typ='node', bbox=nigeria.total_bounds, recurse='down', tags='power')
osm_power_way_nga = osm.query_osm(typ='way', bbox=nigeria.total_bounds, recurse='down', tags='power')

# find places that have a population
places_nga = osm_places_nga[['geometry', 'population', 'name']]
places_nga = sjoin(places_nga, nigeria, how="inner", op="within")
places_nga = places_nga[~pd.isnull(places_nga.population)]

# find length of power line data in nigeria
power_lines_nga = osm_power_way_nga[osm_power_way_nga.geom_type == 'LineString'][['geometry']]
power_lines_nga = sjoin(power_lines_nga, nigeria, how="inner", op="within")

# assign line distances back to geopandas df and add styling to display via geojson.io
power_lines_nga['line_length_m'] = power_lines_nga.geometry.apply(lambda linestring: sum(su.linestring_distances(linestring)))
# style red
power_lines_nga['stroke'] = "#00ff00"

# output as geojson
power_line_json = "/home/cjn/geodata/nga_power_lines_osm.json"
json_file = open(power_line_json, mode='w')
json_file.write(power_lines_nga.to_json())
json_file.close()
