import gpxpy.geo
from Google_Matrix import DM
import urllib2
from collections import defaultdict
import os
import re
import time
import urllib2
import unicodecsv as csv



class Place_Distance(object):
    def __init__(self):
        self.data = defaultdict(list)    
    def read_data(self):
        #Read EXCEL Restaurant data 
        folder = os.path.join(os.getcwd(), "Calculate_distance")
        filename = os.path.join(folder, "restaurant_data.csv")
        data_list = []
        with open(filename, 'rb') as f:
            reader = csv.reader(f, encoding='utf-8')
            next(reader)
            for i in reader:
                data_list.append(i)
        self.data["data_list"] = data_list    

    def read_mrt(self):
        #Read EXCEL MRT data        
        folder = os.path.join(os.path.dirname(os.path.normpath(os.getcwd())), "Mrt", "Mrt_data")
        filename = os.path.join(folder, "final_data.csv")
        data_list = []
        with open(filename, 'rb') as f:
            reader = csv.reader(f, encoding='utf-8')    
            next(reader)
            for i in reader:
                data_list.append(i)
        self.data["mrt_list"] = data_list  
        
    def compare_distance(self,res):        
        val, idx = min((val, idx) for (idx, val) in enumerate(res))
        idx += 2
        return val,idx #Return min_distance, and MRT Index
    def generate_excel(self,name):
        self.read_data() #Read the input file 
        #print name

        folder = os.path.join(os.getcwd(), "Calculate_distance")
        final_list = self.data["data_list"]
        filename = os.path.join(folder, "output_exCel.csv")
        with open(filename, 'wb') as f:  # output csv file
            writer = csv.writer(f, encoding='utf-8')
            header = ["restaurantid", "Restaurant", "Location", "Open", "Phone", "Website", "Latitude", "Longitude", "Json File", "area","Nearest_Mrt"]
            writer.writerow(header)
            final = []

            for count, old in enumerate(final_list):
                old.append(name[count])
                final.append(old)
            for new in final:
                writer.writerow(new)
            print ("See you again....")
    
    def start(self):
        self.read_data()
        self.read_mrt()
        indMrt = {'':''}
        station_list = [] 
        for ind,restaurant in enumerate(self.data["data_list"]):
            temp_distance,temp_rest,mrt_keys = [],{},{}            
            print ("-----DATA ROW-----",ind)
            res_lat,res_lng = float(restaurant[6]),float(restaurant[7])
            for ind,mrt in enumerate(self.data["mrt_list"]):
                ind += 2                
                indMrt[mrt[0]] = ind #MRT data and its index
                mrt_lat,mrt_lng = float(mrt[2]),float(mrt[3])
                distance = gpxpy.geo.haversine_distance(res_lat, res_lng, mrt_lat, mrt_lng)
                mrt_keys[mrt_lat,mrt_lng] = ind 
                temp_distance.append(distance)    
            final_distance,distance_idx = self.compare_distance(temp_distance)
            #print "FINAL",final_distance,distance_idx
            station_name = indMrt.keys()[indMrt.values().index(distance_idx)]            
            #print "Dict",mrt_keys
            print station_name
            station_list.append(station_name)
        self.generate_excel(station_list)
            
place = Place_Distance()
place.start()            
       

