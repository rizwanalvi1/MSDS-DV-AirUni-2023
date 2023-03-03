import configuration as conf

# tmp_list = ['0733_mbtiles','0711_mbtiles','0733_geojson']
# matches = ["0733", "mbtiles"]

# for item in tmp_list:
#     if matches[0] in item:
#         if matches[1] in item:
#             print(item)
#     else:
#         print('No match found..')

# tilejoin_list = []

# for item in conf.item_list:
#     tilejoin_list.append(item)

# print(str(tilejoin_list))

tilejoin_list = '.mbtiles '.join(conf.item_list)+'.mbtiles'
print(tilejoin_list)