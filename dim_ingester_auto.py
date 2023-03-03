import os
import configuration as conf

distinct_district_list = []
# distinct_district_list = ['073325005','071435002','071310007']
# distinct_district_list = ['073325005','073325001']


for filename in os.listdir(conf.directory):
    f = os.path.join(conf.directory, filename)
    if os.path.isfile(f) and '.gpkg' in str(f):
        district_id = filename.split('_')[0]
        distinct_district_list.append(district_id)
        # print(filename)
        print(district_id)
        for item in conf.item_list:
            os_command = 'docker run --rm -v %s:/data osgeo/gdal ogr2ogr -f GeoJSON  -t_srs "EPSG:4326" %s %s %s'%(conf.directory,"/data/output/"+district_id+"_"+item+".geojson","/data/"+district_id+"_output.gpkg",item)
            os.system(os_command)
            print("GeoJSON Generated Successfully : "+item)
            os_command = "docker run --rm -v %s:/data metacollin/tippecanoe tippecanoe -Z8 -z18  -r1 -pk -pf --maximum-tile-bytes=50000 -sEPSG:4326 -S15 -o /data/output/%s_%s.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping /data/output/%s_%s.geojson"%(conf.directory,district_id,item,district_id,item)
            # sudo docker run --rm -v /data:/data mapbox/tippecanoe tippecanoe -Z8 -z18  -r1 -pk -pf --maximum-tile-bytes=50000 -sEPSG:4326 -S15 -o /data/dim/out_dropduct.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping /data/dim/out_dropduct.geojson
            os.system(os_command)
            print("Mbtiles Generated Successfully : "+item)
            os_command = 'docker run --rm -v %s:/data osgeo/gdal ogr2ogr -f "PostgreSQL" -overwrite PG:"host=%s dbname=dim user=postgres SCHEMAS=%s password=mysecretpassword" "/data/output/%s_%s.geojson" -nln %s'%(conf.directory,conf.docker_ip,district_id,district_id,item,str(item).lower())
            # sudo docker run --rm -v /data:/data osgeo/gdal ogr2ogr -f "GeoJSON" -t_srs "EPSG:4326" /data/dim/out_dropduct.geojson PG:"host=172.17.0.1 dbname=dim user=postgres password=mysecretpassword port=5433" "071310007.out_dropduct"
            os.system(os_command)
            print("PostGIS Import Successfull : "+item)

# for district in distinct_district_list:
tilejoin_list = []
for district in distinct_district_list:
    tilejoin_list = []
    for filename in os.listdir(conf.directory+"\\output"):
        # print(filename)
        f = os.path.join(conf.directory, filename)
        if 'mbtiles' in filename:
            filename_prefix = str(filename).split('_')[0]
            if district == filename_prefix:
                tilejoin_list.append(filename)
                    # tilejoin_list = '.mbtiles '.join(conf.item_list)+'.mbtiles'
                tilejoin_str = ' '.join(tilejoin_list)
    tilejoin_str_final = "/data/output/"+str(tilejoin_list).replace("'","").replace('[','').replace(']','').replace(',','').replace(' ',' /data/output/')
    # print(tilejoin_str_final)
    os_command = 'docker run --rm -v %s:/data metacollin/tippecanoe tile-join -o /data/output/%s.mbtiles -pk %s'%(conf.directory,district,tilejoin_str_final)
    os.system(os_command)
    print("TileJoin Process Completed Successfully : ", district)


os_command  = 'docker run --rm -it -v %s\\output:/data -p 8080:8080 maptiler/tileserver-gl --mbtiles %s.mbtiles'%(conf.directory,distinct_district_list[0])
print('Tileserver-gl Starting... ')
os.system(os_command)

        # docker run --rm -v /data:/data mapbox/tippecanoe tile-join -o /data/dim/071310007.mbtiles -pk /data/dim/buildings.mbtiles /data/dim/access_structures.mbtiles /data/dim/out_demandpoints.mbtiles /data/dim/out_distributioncables.mbtiles /data/dim/out_distributionclusters.mbtiles /data/dim/out_distributionpoints.mbtiles /data/dim/out_dropduct.mbtiles /data/dim/out_feedercables.mbtiles

        # 073325005_OUT_DemandPoints.mbtiles
        # 073325005_OUT_DistributionCables.mbtiles
# C:\Users\Administrator\Documents\GitHub\fbr_atl\data\071310007_output.gpkg'
