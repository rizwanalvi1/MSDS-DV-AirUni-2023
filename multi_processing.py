import multiprocessing
import psycopg2
import time
import os
import requests
import json
import configuration as conf

conn = psycopg2.connect(
    host="localhost",
    database="zoneomics_20230220",
    user="postgres",
    password="mysecretpassword"
)
cursor = conn.cursor()

def parallel_function(sql_stmt):
    print(sql_stmt)
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()
    # print(rows)
    for row in rows:
        print("Processing : "+str(row[0]))
        # https://portal.assessor.lacounty.gov/api/parceldetail?ain=2683024011
        url = "https://portal.assessor.lacounty.gov/api/parceldetail?ain="+str(row[0])
        # print(url)
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.content)
            if data['Parcel'] is not None:
                parcel_id = data['Parcel']['AIN']
                lat = data['Parcel']['Latitude']
                lon = data['Parcel']['Longitude']
                situsstreet = data['Parcel']['SitusStreet']
                situscity = data['Parcel']['SitusCity']
                situszipcode = data['Parcel']['SitusZipCode']
                usetypecode = data['Parcel']['UseTypeCode']
                usetype = data['Parcel']['UseType']
                parceltype = data['Parcel']['ParcelType']
                parcelstatus = data['Parcel']['ParcelStatus']

                # print(sql_stmt)
                cursor.execute("INSERT INTO "+conf.info_table_name+"(parcel_id, lat, lon, situsstreet, situscity, situszipcode, usetypecode, usetype, parceltype, parcelstatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                                                            (parcel_id, lat, lon, situsstreet, situscity, situszipcode, usetypecode, usetype, parceltype, parcelstatus))
                conn.commit()
                # print("Parcel processed : "+parcel_id)
            else:
                print('Invalid parcel_id encountered......')
        else:
            print("Error: Could not retrieve data from URL")
    # return sql_stmt

def get_offset_queries(processors, table_name, info_table_name):
    tmp_list = []
    sql_stmt = "select count(*),round(count(*)/{},0) from {} where parcel_id is not null and parcel_id not ilike '%*%'".format(processors,table_name)
    cursor.execute(sql_stmt)
    rows = cursor.fetchall()
    total_size = rows[0][0]
    chunk_size = rows[0][1]

    # print(total_size,chunk_size,"adfs")
    # total_size = 879401
    # chunk_size = 109925
    tmp_var = 0
    for i in range(processors):
        # print(str(i)+" : "+str(round(total_size / (i+1))))
        if i==0:
            # str_tmp = "select parcel_id from (select id,parcel_id from "+table_name+" limit "+str(chunk_size)+" offset "+str(i)+" ) as tab where parcel_id is not null and parcel_id not ilike '%*%' and parcel_id not in (select parcel_id from "+info_table_name+")"
            str_tmp = "select distinct parcel_id as parcel_id from "+table_name+" as tab1 where parcel_id is not null and parcel_id not ilike '%*%' and not exists (select 1 from "+info_table_name+" as tab2 where tab2.parcel_id=tab1.parcel_id) limit "+str(chunk_size)+" offset "+str(i)
            # print(int(time.time()))
            tmp_list.append(str_tmp)
        else: 
            # str_tmp = "select parcel_id from (select id,parcel_id from "+table_name+" limit "+str(chunk_size)+" offset "+str((i+1)*chunk_size)+") as tab where parcel_id is not null and parcel_id not ilike '%*%' and parcel_id not in (select parcel_id from "+info_table_name+")"
            str_tmp = "select distinct parcel_id as parcel_id from "+table_name+" as tab1 where parcel_id is not null and parcel_id not ilike '%*%' and not exists (select 1 from "+info_table_name+" as tab2 where tab2.parcel_id=tab1.parcel_id) limit "+str(chunk_size)+" offset "+str((i+1)*chunk_size)
            # print(int(time.time()))
            tmp_list.append(str_tmp)
    # cursor.close()/
    # conn.close()
    return tmp_list
if __name__ == "__main__":
    # print(os.cpu_count())
    no_of_processors = int(os.cpu_count())
    # no_of_processors = 1
    data_list =  get_offset_queries(no_of_processors,conf.parcel_table_name, conf.info_table_name)
    # for query in data_list:
    #     print(query)
    with multiprocessing.Pool(processes=no_of_processors) as pool:
        pool.map(parallel_function, data_list)
        # ids = cursor.execute(query)
        # for id in ids
# cursor.close()
# conn.close()
