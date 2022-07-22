# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:04:01 2022

@author: jobbo
"""
# import libraries
import processing

# create time list
time_list = []
time_list = list(range(1980,2000,1))+list(range(2020,2040,1))+list(range(2060,2080,1))


# create input file name list
var_list = ['clt','flashrate','hurs','huss','pr','prsn',
            'psl','rls','rss','sfcWind','snw','tas',
            'tasmax','tasmin','uas','vas','wsgmax10m']

# def create_file_name():
#     file_list=[]
#     for index,item in enumerate(time_list):
#         file_list.append('D:\dissertation\CEDA_archive_2.2km_01_clt_manual\clt_rcp85_land-cpm_uk_2.2km_01_mon_{}12-{}11.nc'.format(item,int(item)+1))
#     return file_list

# warp reprojection
def bulk_warp(in_dir, out_dir, crs='EPSG:27700', resolution=2200.00 ):
    processing.run("gdal:warpreproject",
                    {"INPUT":in_dir,
                    "TARGET_CRS":crs,
                    "TARGET_RESOLUTION":resolution,
                    "OUTPUT":out_dir})


# call functions
# loop the .nc files
for var_name in var_list:
    for time_name in time_list:
        if var_name in ['flashrate','tasmax','tasmin']:
            file_name = 'D:\\dissertation\\nc_files\\CEDA_archive_2.2km_01_{}\\{}_rcp85_land-cpm_uk_2.2km_01_day_{}1201-{}1130.nc'.format(var_name,var_name,time_name,int(time_name)+1)
            output_dir = 'D:\\dissertation\\geotiff_files\\{}\\{}_rcp85_land-cpm_uk_2.2km_01_day_{}1201-{}1130.tif'.format(var_name,var_name,time_name,int(time_name)+1)
        else:
            file_name = 'D:\\dissertation\\nc_files\\CEDA_archive_2.2km_01_{}\\{}_rcp85_land-cpm_uk_2.2km_01_mon_{}12-{}11.nc'.format(var_name,var_name,time_name,int(time_name)+1)
            output_dir = 'D:\\dissertation\\geotiff_files\\{}\\{}_rcp85_land-cpm_uk_2.2km_01_mon_{}12-{}11.tif'.format(var_name,var_name,time_name,int(time_name)+1)
        
        bulk_warp(file_name, output_dir)
        
