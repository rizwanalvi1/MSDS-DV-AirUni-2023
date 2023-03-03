import json
import psycopg2
import os

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="dim",
    user="postgres",
    password="mysecretpassword"
)

directory_path = "./district_bbox"
# Get a list of all files in the directory
file_names = os.listdir(directory_path)

for file_name in file_names:
    schema_name = file_name.split('.')[0]
    print(file_name)
    cursor = conn.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS "'+schema_name+'"')
    print(schema_name+" : schema created successfully..")
    conn.commit()
    cursor.execute('CREATE table IF NOT EXISTS "'+schema_name+'".district_boundaries(id serial ,geom geometry(MultiPolygon,25832),district_name text)')
    print(schema_name+" : boundaries table created successfully..")
    conn.commit()
    full_file_path = directory_path+"/"+file_name
    with open(full_file_path) as f:
        data = json.load(f)
    district_name = data['name']
    for feature in data["area"]["features"]:
    # for feature in data["features"]:
        geom = feature["geometry"]
        cursor.execute('insert into "'+schema_name+'".district_boundaries(geom,district_name) values(ST_SetSRID(ST_GeomFromGeoJSON(%s),25832),%s);',
            (json.dumps(geom),district_name)
        )
        print('json bounds have been calculated successfully..')
conn.close()

# load .geojson file
# with open("071110000.geojson") as f:
#     data = json.load(f)
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE geojson_table (id serial PRIMARY KEY, geom geometry(MultiPolygon,25832));")
# # Insert data into table
# for feature in data["area"]["features"]:
#     geom = feature["geometry"]
#     cursor.execute(
#         "INSERT INTO geojson_table (geom) VALUES (ST_SetSRID(ST_GeomFromGeoJSON(%s),25832));",
#         (json.dumps(geom),)
#     )

# # Commit changes and close connection
# conn.commit()
# conn.close()
