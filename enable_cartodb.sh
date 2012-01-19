[ $1 ] || { echo "Specify database name"; exit 1; }

#enable the database named by the input param for postgis AND cartodb
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='"$1"';"

sql_load_list="postgis.sql spatial_ref_sys.sql rtpostgis.sql topology.sql legacy.sql legacy_compatibility_layer.sql"

#load the sql
for file in $sql_load_list; 
do 
  file_path=`find /usr/share/postgresql -name $file`
  if [ -f "$file_path" ]; then
    psql -U postgres -d $1 -f "$file_path"
  else
    echo "$file_path not found, check your postgis installation."
    return -1
  fi
done 

psql -d $1 -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d $1 -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

