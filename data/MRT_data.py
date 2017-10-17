# import pyshp
import shapefile 
import os
import re
import time
import unicodecsv as csv
import simplejson as json
from SVY21 import SVY21

# read the file
myshp = open('C:\\Users\\15043025\\Desktop\\data\\MRTLRTStnPtt.shp', "rb")
mydbf = open('C:\\Users\\15043025\\Desktop\\data\\MRTLRTStnPtt.dbf', "rb")
sf = shapefile.Reader(shp=myshp, dbf=mydbf)
records = sf.shapeRecords()

# check what we have
print 'There are', len(records), 'shape objects in this file'
#print 'Type', sf.shapes()[0].shapeType
#print sf.fields

x = records[0]
#print x.record
#print x.record[1],x.record[2]

#Before convert to SG system
#for record in records[:-1]:
#    print record.record[0], record.shape.points[0]

svy = SVY21()

record_list = [] 
for record in records[:]:
    mrt_name = record.record[1]
    mrt_code = record.record[2]
    latlong = svy.computeLatLon(record.shape.points[0][1], record.shape.points[0][0]) #Tuple
    
    print mrt_name,mrt_code
    print latlong[0],latlong[1]
    print ("")
    record_list.append([mrt_name,mrt_code,latlong[0],latlong[1]])
    


def save_final(input_list):
    folder = os.path.join(os.getcwd(), "Mrt_data")
    final_list = input_list
    filename = os.path.join(folder, "final_data.csv")
    with open(filename, 'wb') as f:
        writer = csv.writer(f, encoding='utf-8')
        header = ["MRT_Name", "MRT_Code", "Lat","Long"]
        writer.writerow(header)
        for i in final_list:
            writer.writerow(i)
save_final(record_list)
print ("Python File loaded succesfully")