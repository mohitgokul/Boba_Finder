#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
import googlemaps
import geocoder
import requests
from geopandas import GeoDataFrame
from shapely.geometry import Point
from geojsonio import display
import mpu
import sys



def mpu_distance(point1, point2):
    return mpu.haversine_distance(point1, point2)


def compute(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address, 'key':'AIzaSyAuW05COfvNht0F7rIZkdtSiimRRbzdjns'}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    return (location['lat'], location['lng'])


class BubbleTea(object):

    # authentication initialized
    gmaps = googlemaps.Client(key='AIzaSyAuW05COfvNht0F7rIZkdtSiimRRbzdjns')
    

    def __init__(self, filename):
        self.boba = pd.read_csv(filename)[:num_shops]
#         self.boba = self.boba[:10]
        self.length = len(self.boba)
    
    def calc_coords(self, user_address): 
        self.boba['Lat'] = [compute(val)[0] for val in self.boba['Address']]
        self.boba['Long'] = [compute(val)[1] for val in self.boba['Address']]
        self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Long, self.boba.Lat)]
        user_coord = compute(user_address)
        self.boba['distance'] = [mpu_distance(user_coord, (self.boba.Lat[i], self.boba.Long[i])) for i in range(self.length)]

    def sort_by_distance(self, count):
        self.boba = self.boba.sort_values(by=['distance'])[:count]
        
    def get_geo(self):
        return(list(self.boba['Coordinates']))
    
    def get_names(self):
        return(self.boba['Name'])
     
    def get_gdf(self):
        crs = {'init': 'epsg:4326'}
        return(GeoDataFrame(self.get_names(), crs=crs, geometry=self.get_geo()))
    
    def visualize(self):
        self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Long, self.boba.Lat)]
        updated = self.get_gdf()
        display(updated.to_json())
    
    def get_closest(self):
        self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Long, self.boba.Lat)]
        updated = self.get_gdf()
        display(updated.to_json())
        

num_shops, addr = int(sys.argv[1]), sys.argv[2]


boba = BubbleTea("./boba.csv")


boba.calc_coords(addr)
#boba.boba

boba.sort_by_distance(6)
#boba.boba

boba.visualize()
