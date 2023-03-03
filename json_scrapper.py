import requests
import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="zoneomics_20230220",
    user="postgres",
    password="mysecretpassword"
)

cursor = conn.cursor()
cursor.execute("select distinct parcel_id from usa_california_los_angeles_parcels where parcel_id is not null and parcel_id not ilike '%*%' and parcel_id not in (select parcel_id from usa_california_los_angeles_info)")
rows = cursor.fetchall()

for row in rows:
    print("Processing : "+str(row[0]))
    url = "https://portal.assessor.lacounty.gov/api/parceldetail?ain="+str(row[0])

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
            cursor.execute("INSERT INTO usa_california_los_angeles_info(parcel_id, lat, lon, situsstreet, situscity, situszipcode, usetypecode, usetype, parceltype, parcelstatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                                                        (parcel_id, lat, lon, situsstreet, situscity, situszipcode, usetypecode, usetype, parceltype, parcelstatus))
            conn.commit()
            # print("Parcel processed : "+parcel_id)
        else:
            print('Invalid parcel_id encountered......')
    else:
        print("Error: Could not retrieve data from URL")

cursor.close()
conn.close()
    