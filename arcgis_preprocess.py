# import libraries
import pandas as pd
import numpy as np
import arcpy
from arcpy import env
from arcpy.sa import *
import datetime
import os, sys
import time
import pymongo
from pymongo import MongoClient


# input file
# root_dir = 'D:\\dissertation\\geotiff_files\\'
# out_root = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\output\\'
# env.workspace = 'D:\dissertation\geotiff_files\clt\clt_rcp85_land-cpm_uk_2.2km_01_mon_198012-198111.tif'


# To allow overwriting the output change the overwrite option to true in ArcGIS Pro
arcpy.env.overwriteOutput = True


# # Set variables
# env.workspace = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss'

var_list = ['clt','flashrate','hurs','huss','pr','prsn',
            'psl','rls','rss','sfcWind','snw','tas',
            'tasmax','tasmin','uas','vas','wsgmax10m']

var_list_short = ['clt','flash','hurs','huss','pr','prsn',
            'psl','rls','rss','sfcWind','snw','tas',
            'tasmax','tasmin','uas','vas','wsgmax']

time_list_1yr = list(range(1980,2000,1))+list(range(2020,2040,1))+list(range(2060,2080,1))

time_list_20yr = ['1980','2020','2060']

band_list_mon_1yr = ['Band_'+str(i) for i in list(range(1,13,1))]

band_list_mon_20yr = ['Band_'+str(i) for i in list(range(1,241,1))]

band_list_day = ['Band_'+str(i) for i in list(range(1,361,1))]

seasons = ['winter','spring','summer','autumn']

# Create seasonal files
# # 1. Cell statistics function - seasonal map
# def CELL_STATS(in_rasters, out_dir, stats_type, ignore_nodata='DATA', multiband='SINGLE_BAND'):
#     outCellStats = CellStatistics(in_rasters, stats_type, ignore_nodata, multiband)
#     outCellStats.save(out_dir)

# # Call CELL_STATS function
# # ['Band_1','Band_2','Band_3','Band_4']
# for var_name in var_list:
#     if var_name == 'wsgmax10m':
#         for time_name in time_list_20yr:
#             env.workspace = root_dir + 'wsgmax10m\\wsgmax10m_rcp85_land-cpm_uk_2.2km_01_mon_{}12-{}11.tif'.format(time_name,int(time_name)+20)
#             for index, band_name in enumerate(band_list_mon_20yr):
#                 if index%3 != 0:
#                     continue
#                 if band_name == band_list_mon_20yr[len(band_list_mon_20yr)-2]:
#                     break
#                 rasters = [band_name, band_list_mon_20yr[index+1], band_list_mon_20yr[index+2]]
#                 year = str(int(time_name)+index//12)
#                 season = seasons[index%4]
#                 out_dir = out_root + '{}\\{}_{}.tif'.format(var_name,year,season)
#                 CELL_STATS(rasters, out_dir, 'MEAN')

#     elif var_name in ['flashrate','tasmax','tasmin']:
#         for time_name in time_list_1yr:
#             env.workspace = root_dir + '{}\\{}_rcp85_land-cpm_uk_2.2km_01_day_{}1201-{}1130.tif'.format(var_name, var_name, time_name,int(time_name)+1)
#             # some hard code here
#             for i in range(4): 
#                 season = seasons[i]
#                 rasters = ['Band_'+str(j) for j in list(range(90*i+1,90*i+91,1))]
#                 out_dir = out_root + '{}\\{}_{}.tif'.format(var_name,time_name,season)
#                 CELL_STATS(rasters, out_dir, 'MEAN')

#     else:
#         for time_name in time_list_1yr:
#             env.workspace = root_dir + '{}\\{}_rcp85_land-cpm_uk_2.2km_01_mon_{}12-{}11.tif'.format(var_name, var_name, time_name,int(time_name)+1)
#             for i in range(4): 
#                 season = seasons[i]
#                 rasters = ['Band_'+str(j) for j in list(range(3*i+1,3*i+4,1))]
#                 out_dir = out_root + '{}\\{}_{}.tif'.format(var_name,time_name,season)
#                 CELL_STATS(rasters, out_dir, 'MEAN')         


# # 2. Extract by mask
# in_lyr_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\rasters\\'
# in_mask = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\GBR_adm\\GBR_adm0.shp'
# out_mask_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_extract\\'

# def MASK_EXTRACT(in_root_dir, mask, out_dir=out_mask_dir):
#     for var_name in var_list:
#         for year_num in time_list_1yr:
#             for season_name in seasons:
#                 target_file = in_root_dir + '{}_{}_{}Lyr.lyrx'.format(var_name,year_num,season_name)
#                 outExtractByMask = ExtractByMask(target_file,mask)
#                 outExtractByMask.save(out_dir + '{}_{}_{}Mask.tif'.format(var_name,year_num,season_name))

# MASK_EXTRACT(in_lyr_dir,in_mask)


# # 3. Find maximum and minimum value for each variable
# in_mask_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_extract\\'

# # Create a dict to store values
# var_dict_max = dict.fromkeys(var_list)
# var_dict_min = dict.fromkeys(var_list)

# def find_extremes():
#     for var_name in var_list:
#         raster_file_first = in_mask_dir + '{}_1980_winterMask.tif'.format(var_name)
#         max_val = arcpy.management.GetRasterProperties(raster_file_first,'MAXIMUM').getOutput(0) 
#         min_val = arcpy.management.GetRasterProperties(raster_file_first,'MINIMUM').getOutput(0) 
#         for year_num in time_list_1yr:
#             for season_name in seasons:
#                 raster_file = in_mask_dir + '{}_{}_{}Mask.tif'.format(var_name,year_num,season_name)
#                 if arcpy.management.GetRasterProperties(raster_file,'MAXIMUM').getOutput(0) > max_val:
#                     max_val = arcpy.management.GetRasterProperties(raster_file,'MAXIMUM').getOutput(0)
#                 if arcpy.management.GetRasterProperties(raster_file,'MINIMUM').getOutput(0) < min_val:
#                     min_val = arcpy.management.GetRasterProperties(raster_file,'MINIMUM').getOutput(0)
#         var_dict_max[var_name] = max_val
#         var_dict_min[var_name] = min_val

# find_extremes()
# print(var_dict_max,var_dict_min)


# # 4.Change symbology
# # 4.1 Input geotiff and save as .lyr file (layer file)
# in_tiff_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_extract\\'
# def MAKE_RASTER_LAYER(in_raster,out_raster):
#     arcpy.management.MakeRasterLayer(in_raster,out_raster)

# def MAKE_LAYER_FILE(in_root_dir):
#     for var_name in var_list:
#         for year_num in time_list_1yr:
#             for season_name in seasons:
#                 target_file = in_root_dir + '{}_{}_{}Mask.tif'.format(var_name,year_num,season_name)
#                 out_raster = '{}_{}_{}'.format(var_name,year_num,season_name)
#                 MAKE_RASTER_LAYER(target_file,out_raster)
#                 arcpy.SaveToLayerFile_management(out_raster,'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_layer_file\\{}_{}_{}.lyr'.format(var_name,year_num,season_name),'ABSOLUTE')

# MAKE_LAYER_FILE(in_tiff_dir)

# # 4.2 Add all layers to map
# p = arcpy.mp.ArcGISProject('C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_test.aprx')
# m = p.listMaps('Map')[0]
# in_mLyr_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_layer_file\\'

# for var_name in var_list:
#     for year_name in time_list_1yr:
#         for season_name in seasons:
#             data_path = in_mLyr_dir + '{}_{}_{}.lyrx'.format(var_name,year_name,season_name)
#             m.addDataFromPath(data_path)

# print('added all layers')

# # 4.3 Use 'RasterStretchColorize' to set the stretch symbology for all layers (set min and max)
# # create symbology dicts
# symb_dict = dict.fromkeys(var_list)
# symb_dict['clt'] = 'Shadow to Sunshine'
# symb_dict['flashrate'] = 'Cyan to Purple'
# symb_dict['hurs'] = 'Green-Blue (Continuous)'
# symb_dict['huss'] = 'Green-Blue (Continuous)'
# symb_dict['pr'] = 'Precipitation'
# symb_dict['prsn'] = 'Brown-Green (Continuous)'
# symb_dict['psl'] = 'Red-Blue (Continuous)'
# symb_dict['rls'] = 'Spectral (Continuous)'
# symb_dict['rss'] = 'Spectrum-Full Bright'
# symb_dict['sfcWind'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['snw'] = 'Surface'
# symb_dict['tas'] = 'Prediction'
# symb_dict['tasmax'] = 'Prediction'
# symb_dict['tasmin'] = 'Prediction'
# symb_dict['uas'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['vas'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['wsgmax10m'] = 'Yellow-Green-Blue (Continuous)'

# invert_dict = {'clt':True, 'flashrate':False, 'hurs':False, 'huss':False, 'pr':False,
# 'prsn':False, 'psl':True, 'rls':False, 'rss':False, 'sfcWind':False, 'snw':False,
# 'tas':False, 'tasmax':False, 'tasmin':False, 'uas':False, 'vas':False, 'wsgmax10m':False}

# min_dict = {'clt':30, 'flashrate':0, 'hurs':50, 'huss':0, 'pr':0,
# 'prsn':0, 'psl':1000, 'rls':-90, 'rss':10, 'sfcWind':3, 'snw':0,
# 'tas':-0.5, 'tasmax':0, 'tasmin':-3, 'uas':-0.5, 'vas':-0.5, 'wsgmax10m':3}

# max_dict = {'clt':100, 'flashrate':1, 'hurs':100, 'huss':9, 'pr':10,
# 'prsn':9, 'psl':1025, 'rls':-10, 'rss':90, 'sfcWind':9, 'snw':500,
# 'tas':30, 'tasmax':37, 'tasmin':10, 'uas':8, 'vas':8, 'wsgmax10m':20}

# # change symbology for each variable
# for var_name in var_list:
#     for year_name in time_list_1yr:
#         for season_name in seasons:
#             layer_name = '{}_{}_{}'.format(var_name,year_name,season_name)
#             l = m.listLayers(layer_name)[0]
#             sym = l.symbology

#             if hasattr(sym, 'colorizer'):
#                 if sym.colorizer.type == 'RasterStretchColorizer':
#                     sym.colorizer.stretchType = "MinimumMaximum"
#                     cr = p.listColorRamps(symb_dict[var_name])[0]
#                     sym.colorizer.colorRamp = cr
#                     sym.colorizer.invertColorRamp = invert_dict[var_name]
#                     sym.colorizer.gamma = 2
#                     sym.colorizer.minLabel = str(min_dict[var_name])
#                     sym.colorizer.maxLabel = str(max_dict[var_name])

#                     l.symbology = sym 

#                     #use CIM to set custom statistics
#                     cim_lyr = l.getDefinition('V2')
#                     cim_lyr.colorizer.statsType = 'GlobalStats'
#                     cim_lyr.colorizer.useCustomStretchMinMax = True
#                     cim_lyr.colorizer.stretchStats.max = int(max_dict[var_name])
#                     cim_lyr.colorizer.stretchStats.min = int(min_dict[var_name])
#                     l.setDefinition(cim_lyr)
    
#     print(var_name)

# # save to a new project
# p.saveACopy('C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_Symb_MinMax_ALL.aprx')        


# # Create periodical files (work)
# # 5. Use Cell Statistics to create periodic mean for each variable
# # Save mask_symbology layers of arcgis project to file


# # Check out the ArcGIS Spatial Analyst extension license
# arcpy.CheckOutExtension("Spatial")

# # Set the analysis environments
# arcpy.env.workspace = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\mask_layer_file\\"

# out_period_dir = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_output\\"

periods = ['history','current','future']
ann_seasons = ['annual','winter','spring','summer','autumn']
# # for var_name in var_list:
# #     for season_name in seasons:
# #         for i in range(3):
# #             period_var_list = ['{}_{}_{}.lyrx'.format(var_name,str(i),season_name) for i in list(range(1980+40*i,2000+40*i,1))]
# #             outCellStatistics = CellStatistics(period_var_list, "MEAN", "NODATA", "SINGLE_BAND")
# #             outCellStatistics.save(out_period_dir + "{}_{}_{}.tif".format(var_name,periods[i],season_name))
    
# # arcpy.env.workspace = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_output\\" 

# # for var_name in var_list:
# #     for i in range(3):
# #         period_var_list = ['{}_{}_{}.tif'.format(var_name,periods[i],j) for j in seasons]
# #         outCellStatistics = CellStatistics(period_var_list, "MEAN", "NODATA", "SINGLE_BAND")
# #         outCellStatistics.save(out_period_dir + "{}_{}_{}.tif".format(var_name,periods[i],'annual'))


# # 4.Change symbology
# # 4.1 Input geotiff and save as .lyr file (layer file)
# in_tiff_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_output\\'
# def MAKE_RASTER_LAYER(in_raster,out_raster):
#     arcpy.management.MakeRasterLayer(in_raster,out_raster)

# def MAKE_LAYER_FILE(in_root_dir):
#     for var_name in var_list:
#         for period_name in periods:
#             for season_name in ann_seasons:
#                 target_file = in_root_dir + '{}_{}_{}.tif'.format(var_name,period_name,season_name)
#                 out_raster = '{}_{}_{}'.format(var_name,period_name,season_name)
#                 MAKE_RASTER_LAYER(target_file,out_raster)
#                 arcpy.SaveToLayerFile_management(out_raster,'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_layer_file\\{}_{}_{}.lyr'.format(var_name,period_name,season_name),'ABSOLUTE')

# MAKE_LAYER_FILE(in_tiff_dir)

# # 4.2 Add all layers to map
# p = arcpy.mp.ArcGISProject('C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_test.aprx')
# m = p.listMaps('Map')[0]
# in_mLyr_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_layer_file\\'

# for var_name in var_list:
#     for period_name in periods:
#         for season_name in ann_seasons:
#             data_path = in_mLyr_dir + '{}_{}_{}.lyrx'.format(var_name,period_name,season_name)
#             m.addDataFromPath(data_path)

# print('added all layers')

# # 4.3 Use 'RasterStretchColorize' to set the stretch symbology for all layers (set min and max)
# # create symbology dicts
# symb_dict = dict.fromkeys(var_list)
# symb_dict['clt'] = 'Shadow to Sunshine'
# symb_dict['flashrate'] = 'Cyan to Purple'
# symb_dict['hurs'] = 'Green-Blue (Continuous)'
# symb_dict['huss'] = 'Green-Blue (Continuous)'
# symb_dict['pr'] = 'Precipitation'
# symb_dict['prsn'] = 'Brown-Green (Continuous)'
# symb_dict['psl'] = 'Red-Blue (Continuous)'
# symb_dict['rls'] = 'Spectral (Continuous)'
# symb_dict['rss'] = 'Spectrum-Full Bright'
# symb_dict['sfcWind'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['snw'] = 'Surface'
# symb_dict['tas'] = 'Prediction'
# symb_dict['tasmax'] = 'Prediction'
# symb_dict['tasmin'] = 'Prediction'
# symb_dict['uas'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['vas'] = 'Yellow-Green-Blue (Continuous)'
# symb_dict['wsgmax10m'] = 'Yellow-Green-Blue (Continuous)'

# invert_dict = {'clt':True, 'flashrate':False, 'hurs':False, 'huss':False, 'pr':False,
# 'prsn':False, 'psl':True, 'rls':False, 'rss':False, 'sfcWind':False, 'snw':False,
# 'tas':False, 'tasmax':False, 'tasmin':False, 'uas':False, 'vas':False, 'wsgmax10m':False}

# min_dict = {'clt':30, 'flashrate':0, 'hurs':50, 'huss':0, 'pr':0,
# 'prsn':0, 'psl':1000, 'rls':-90, 'rss':10, 'sfcWind':3, 'snw':0,
# 'tas':-0.5, 'tasmax':0, 'tasmin':-3, 'uas':-0.5, 'vas':-0.5, 'wsgmax10m':3}

# max_dict = {'clt':100, 'flashrate':1, 'hurs':100, 'huss':9, 'pr':10,
# 'prsn':9, 'psl':1025, 'rls':-10, 'rss':90, 'sfcWind':9, 'snw':500,
# 'tas':30, 'tasmax':37, 'tasmin':10, 'uas':8, 'vas':8, 'wsgmax10m':20}

# # change symbology for each variable
# for var_name in var_list:
#     for period_name in periods:
#         for season_name in ann_seasons:
#             layer_name = '{}_{}_{}'.format(var_name,period_name,season_name)
#             l = m.listLayers(layer_name)[0]
#             sym = l.symbology

#             if hasattr(sym, 'colorizer'):
#                 if sym.colorizer.type == 'RasterStretchColorizer':
#                     sym.colorizer.stretchType = "MinimumMaximum"
#                     cr = p.listColorRamps(symb_dict[var_name])[0]
#                     sym.colorizer.colorRamp = cr
#                     sym.colorizer.invertColorRamp = invert_dict[var_name]
#                     sym.colorizer.gamma = 2
#                     sym.colorizer.minLabel = '<' + str(min_dict[var_name]) 
#                     sym.colorizer.maxLabel = '>' + str(max_dict[var_name])

#                     l.symbology = sym 

#                     #use CIM to set custom statistics
#                     cim_lyr = l.getDefinition('V2')
#                     cim_lyr.colorizer.statsType = 'GlobalStats'
#                     cim_lyr.colorizer.useCustomStretchMinMax = True
#                     cim_lyr.colorizer.stretchStats.max = int(max_dict[var_name])
#                     cim_lyr.colorizer.stretchStats.min = int(min_dict[var_name])
#                     l.setDefinition(cim_lyr)
    
#     print(var_name)

# # save to a new project
# p.saveACopy('C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_Symb_MinMax_Period.aprx')        





# # 5. Share as web layer
# # Sign in to portal
# # arcpy.SignInToPortal("https://www.arcgis.com", "h59201yo", "Oyb9865761885!")
# # arcpy.SignInToPortal("https://UoManchester.maps.arcgis.com", "yunbei.ou@student.manchester.ac.uk", "Oyb9865761885!")
# # print('signed in successfully')

# # Set output file names
# outdir = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\Service_definition"

# # Reference map to publish
# prjPath = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_Symb_MinMax_ALL.aprx"
# aprx = arcpy.mp.ArcGISProject(prjPath)
# m = aprx.listMaps('Map')[0]

# for var_name in var_list:
#     if var_name == 'clt' or var_name == 'flashrate' or var_name == 'hurs' or var_name == 'huss':
#         continue
#     for year_name in time_list_1yr:
#         for season_name in seasons:
#             lyr = m.listLayers('{}_{}_{}'.format(var_name,year_name,season_name))[0]

#             # Create TileSharingDraft and set service properties
#             service = '{}_{}_{}'.format(var_name,year_name,season_name)
#             sddraft_filename = service + ".sddraft"
#             sddraft_output_filename = os.path.join(outdir, sddraft_filename)
#             sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service, lyr)
#             sharing_draft.summary = "UKCP18_{}_{}_{}".format(var_name,year_name,season_name)
#             sharing_draft.tags = "UKCP18_{}_{}_{}".format(var_name,year_name,season_name)

#             # Create Service Definition Draft file
#             sharing_draft.exportToSDDraft(sddraft_output_filename)

#             # Stage Service
#             sd_filename = service + ".sd"
#             sd_output_filename = os.path.join(outdir,sd_filename)
#             arcpy.server.StageService(sddraft_output_filename,sd_output_filename)

#             # Share to portal
#             print("Uploading Service Definition of {}_{}_{}...".format(var_name,year_name,season_name))
#             arcpy.server.UploadServiceDefinition(sd_output_filename,"My Hosted Services", in_public = "PUBLIC", in_organization = "SHARE_ORGANIZATION")

#             print("Successfully upload service of {}_{}_{}.".format(var_name,year_name,season_name))


# # 6. Change cache tiles (manage-map-server-cache-tiles)
# # Sign in to portal (if it is signed in out of python, skip this step)
# # arcpy.SignInToPortal("https://www.arcgis.com", "h59201yo", "Oyb9865761885!") 

# # List of input variables for map service
# scales = [10000000,5000000,1000000,500000,250000]
# updateMode = "RECREATE_ALL_TILES"

# # Variables for reporting
# currentTime = datetime.datetime.now()
# arg1 = currentTime.strftime("%H-%M")
# arg2 = currentTime.strftime("%Y-%m-%d %H:%M")
# file = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\report\\report_%s.txt' % arg1

# # Print results of the script to a report
# report = open(file,'w')

# input_service = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/Extract_19821_0_11/MapServer'

# try:
#     result = arcpy.server.ManageMapServerCacheTiles(input_service , scales, updateMode)
#     while result.status < 4:
#         time.sleep(0.2)
#     resultValue = result.getMessages()
#     report.write ("completed " + str(resultValue))

#     print ("Created cache tiles for given schema successfully for hosted service")
    
# except Exception as e:
#     # If an error occurred, print line number and error message
#     import traceback, sys
#     tb = sys.exc_info()[2]
#     report.write("Failed at step 1 \n" "Line %i" % tb.tb_lineno)
#     report.write(e.message)
# report.close()

# print ("Completed update of cache tiles for hosted service")



# # Previous version (worked)
# # 5. Share as web layer
# # Sign in to portal
# # arcpy.SignInToPortal("https://www.arcgis.com", "h59201yo", "Oyb9865761885!")

# # Set output file names
# outdir = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\Service_definition"

# # Reference map to publish
# prjPath = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_Symb_MinMax_Period.aprx"
# # prjPath = "C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\MyProject_MSc_Diss_Symb_MinMax_ALL.aprx"
# aprx = arcpy.mp.ArcGISProject(prjPath)
# m = aprx.listMaps('Map')[0]

# # out_layer_file = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\output\\save_LYR.lyr'

# # arcpy.SaveToLayerFile_management(m.listLayers('clt_1982_autumn')[0], out_layer_file, "ABSOLUTE")
# # m.addDataFromPath('C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\output\\save_LYR.lyrx')
# # aprx.save()
# # m = aprx.listMaps('Map')[0]
# l = m.listLayers('clt_history_spring')[0]


# # Create TileSharingDraft and set service properties
# service = 'TestWebSharing_15'
# sddraft_filename = service + ".sddraft"
# sddraft_output_filename = os.path.join(outdir, sddraft_filename)
# sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service, l)
# sharing_draft.summary = "UKCP_test_1"
# sharing_draft.tags = "clt_test_1"
# sharing_draft.overwriteExistingService = 'overwriteService'

# # Create Service Definition Draft file
# sharing_draft.exportToSDDraft(sddraft_output_filename)

# # Stage Service
# sd_filename = service + ".sd"
# sd_output_filename = os.path.join(outdir,sd_filename)
# # arcpy.server.StageService(sddraft_output_filename,sd_output_filename)
# arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

# # Share to portal
# print("Uploading Service Definition...")
# # arcpy.server.UploadServiceDefinition(sd_output_filename,"My Hosted Services",in_override='OVERRIDE_DEFINITION',
# # in_public='PUBLIC',in_organization='SHARE_ORGANIZATION')
# output = arcpy.UploadServiceDefinition_server(sd_output_filename,"My Hosted Services",in_override='OVERRIDE_DEFINITION',
# in_public='PUBLIC',in_organization='SHARE_ORGANIZATION')

# print("Successfully upload service.")


# # 6. Change cache tiles (manage-map-server-cache-tiles)
# # Sign in to portal (if it is signed in out of python, skip this step)
# # arcpy.SignInToPortal("https://www.arcgis.com", "h59201yo", "Oyb9865761885!") 

# # List of input variables for map service
# scales = [10000000,5000000,1000000,500000,250000]
# updateMode = "RECREATE_ALL_TILES"

# # Variables for reporting
# currentTime = datetime.datetime.now()
# arg1 = currentTime.strftime("%H-%M")
# arg2 = currentTime.strftime("%Y-%m-%d %H:%M")
# file = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\report\\report_%s.txt' % arg1

# # Print results of the script to a report
# report = open(file,'w')

# # input_service = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/Extract_19821_0_11/MapServer'
# input_service = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_1982_autumn_private/MapServer'

# try:
#     result = arcpy.server.ManageMapServerCacheTiles(input_service , scales, updateMode)
#     print(result)
#     while result.status < 4:
#         time.sleep(0.2)
#     resultValue = result.getMessages()
#     report.write ("completed " + str(resultValue))

#     print ("Created cache tiles for given schema successfully for hosted service")
    
# except Exception as e:
#     # If an error occurred, print line number and error message
#     import traceback, sys
#     tb = sys.exc_info()[2]
#     report.write("Failed at step 1 \n" "Line %i" % tb.tb_lineno)
#     report.write(e.message)
# report.close()

# print ("Completed update of cache tiles for hosted service")


# 7. Data querying - get values for each msoa 
# 7.1 Read the attribute names (NAME_2)
name2_field_name = 'NAME_2'
authorities_list = []
authorities_list_nospace = []
fields = [name2_field_name]

cursor = arcpy.SearchCursor('C:/Users/jobbo/Documents/ArcGIS/Projects/MyProject_MSc_Diss/GBR_adm/GBR_adm2.shp',
fields)

for row in cursor:
    authorities_list.append(row.NAME_2)

del cursor

for i in authorities_list:
    # print(i)
    i = i.replace(" ", "_")
    i = i.replace(",", "_")
    authorities_list_nospace.append(i)
    
print(authorities_list)
print(authorities_list_nospace)

# # 7.2 Extract by mask
# in_lyr_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\period_layer_file\\'
# in_mask = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\msoa_mask\\'
# out_mask_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\msoa_mask_nospace\\'

# def MASK_EXTRACT_MSOA(in_root_dir, mask, out_dir=out_mask_dir):
#     for var_name in var_list:
#         for period_name in periods:
#             for season_name in ann_seasons:
#                 for index, authority_name in enumerate(authorities_list):
#                     target_file = in_root_dir + '{}_{}_{}.lyrx'.format(var_name,period_name,season_name)
#                     mask_dir = mask + '{}.shp'.format(authority_name)
#                     outExtractByMask = ExtractByMask(target_file,mask_dir)
#                     outExtractByMask.save(out_dir + '{}_{}_{}_{}.tif'.format(var_name,period_name,season_name,authorities_list_nospace[index]))

# MASK_EXTRACT_MSOA(in_lyr_dir,in_mask)

# # 7.3 Band Collection Statistics
# # Set environment settings
# env.workspace = "C:/Users/jobbo/Documents/ArcGIS/Projects/MyProject_MSc_Diss/msoa_mask_nospace/"
# outStat_dir = "C:/Users/jobbo/Documents/ArcGIS/Projects/MyProject_MSc_Diss/txt_stats_sep/"

# # save result to different folders
# for var_name in var_list:
#     for period_name in periods:
#         for season_name in ann_seasons:
#             for authority_name in authorities_list_nospace:
#                 inRasterBand1 = '{}_{}_{}_{}.tif'.format(var_name,period_name,season_name,authority_name)
#                 outStatFile = outStat_dir + "{}/".format(var_name) + "{}_{}_{}_{}.txt".format(var_name,period_name,season_name,authority_name)
#                 BandCollectionStats([inRasterBand1], outStatFile)


# # 8. Read .txt and import data to database
# # 8.1 make a connection with MongoClient
# client = MongoClient('localhost', 27017)

# # get database
# db_name = 'UKCP18_test'
# db = client[db_name]

# # 8.2 Read .txt file
# # read .txt file
# txt_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\txt_stats_sep\\'

# 8.3 function to extract value
def read_stat(stat_line):
    pass_one, pass_min, pass_max, pass_mean, pass_std, to_min, to_max, to_mean, to_std = False, False, False, False, False, False, False, False, False
    min_val, max_val, mean_val, std_val = '', '', '', ''

    for i in stat_line:
        if i == ' ' and pass_one == False:
            continue
        elif i == '1' and pass_one == False:
            pass_one = True
            continue
        elif i == ' ' and to_min == False:
            continue
        elif i != ' ' and pass_one == True and pass_min == False:
            to_min = True
            min_val += i
            continue
        elif i == ' ' and to_min == True and to_max == False:
            pass_min = True
            continue
        elif i != ' ' and pass_min == True and pass_max == False:
            to_max = True
            max_val += i
            continue
        elif i == ' ' and to_max == True and to_mean == False:
            pass_max = True
            continue
        elif i != ' ' and pass_max == True and pass_mean == False:
            to_mean = True
            mean_val += i
            continue
        elif i == ' ' and to_mean == True and to_std == False:
            pass_mean = True
            continue
        elif i != ' ' and i != '\n' and pass_mean == True and pass_std == False:
            to_std = True
            std_val += i 
            continue

    return min_val, max_val, mean_val, std_val

# # 8.4 loop the .txt to extract value and insert document to mongodb
# for var_name in var_list:
#     # get collection
#     collection = db[var_name]
#     for period_name in periods:
#         for season_name in ann_seasons:
#             for index, authority_name in enumerate(authorities_list_nospace):
#                 # read file and line 7
#                 file = open(txt_dir + "{}\\".format(var_name) + "{}_{}_{}_{}.txt".format(var_name,period_name,season_name,authority_name))
#                 stat_line = file.readlines()[6]
#                 print(var_name,period_name,season_name,authority_name,stat_line)
#                 file.close()

#                 # read stat values
#                 min_val, max_val, mean_val, std_val = read_stat(stat_line)

#                 # insert a document
#                 collection.insert_one(
#                     {
#                         "_id":"{}_{}_{}_{}".format(var_name,period_name,season_name,authority_name),
#                         "period":period_name,
#                         "season":season_name,
#                         "authority": authorities_list[index],
#                         "authority_nospace":authority_name,
#                         "min_val":min_val,
#                         "max_val":max_val,
#                         "mean_val":mean_val,
#                         "std_val":std_val
#                     }
#                 )

#                 print("Finished:{}_{}_{}_{}".format(var_name,period_name,season_name,authority_name))


# 9. Add msoa values to arcgis attribute table
# read .txt file
txt_dir = 'C:\\Users\\jobbo\\Documents\\ArcGIS\\Projects\\MyProject_MSc_Diss\\txt_stats_sep\\'

# # 9.1 Add fields in attribute table
# arcpy.env.workspace = 'C:/Users/jobbo/Documents/ArcGIS/Projects/MyProject_MSc_Diss/GBR_adm/GBR_adm2.shp'
# for var_name in var_list_short:
#     for i in list(range(3)):
#         for j in list(range(4)):
#             field_name = '{}{}{}'.format(var_name,str(i),str(j))
#             arcpy.AddField_management('GBR_adm2',field_name,'FLOAT')

# 9.2 loop the .txt to extract value and put in dataframe
COLUMN_NAMES = ['authority','var','period','season','value']

df = pd.DataFrame(columns=COLUMN_NAMES)

for var_name in var_list:
    for period_name in periods:
        for season_name in seasons:
            for index, authority_name in enumerate(authorities_list_nospace):
                # read file and line 7
                file = open(txt_dir + "{}\\".format(var_name) + "{}_{}_{}_{}.txt".format(var_name,period_name,season_name,authority_name))
                stat_line = file.readlines()[6]
                print(var_name,period_name,season_name,authority_name,stat_line)
                file.close()

                # read stat values
                min_val, max_val, mean_val, std_val = read_stat(stat_line)

                df = df.append({'authority': authority_name,'var':var_name,'period':period_name,'season':season_name,'value':mean_val}, ignore_index=True)

df = pd.pivot(df, index=['authority'],columns=['var','period','season'],values='value')
print(df)

# 9.3 Insert into attribute table in ArcGIS
# Open an UpdateICursor
fields = []
for var_name in var_list_short:
    for i in list(range(3)):
        for j in list(range(4)):
            fields.append('{}{}{}'.format(var_name,str(i),str(j)))

cursor = arcpy.UpdateCursor('C:/Users/jobbo/Documents/ArcGIS/Projects/MyProject_MSc_Diss/GBR_adm/GBR_adm2.shp',fields)
print('cursor set')

# Insert new values
row_num = 0
for row in cursor:
    authority_name = row.NAME_2
    authority_name = authority_name.replace(" ", "_")
    authority_name = authority_name.replace(",", "_")

    for index_v, var_name in enumerate(var_list):
        for index_p, period_name in enumerate(periods):
            for index_s, season_name in enumerate(seasons):
                set_val = df.loc['{}'.format(authority_name),'{}'.format(var_name)][period_name][season_name]
                row.setValue('{}{}{}'.format(var_list_short[index_v],str(index_p),str(index_s)), set_val)
                row_num += 1
                cursor.updateRow(row)
                print('set in attribute table: {}'.format('{}{}{}'.format(var_list_short[index_v],str(index_p),str(index_s))))

del cursor
print('all value inserted')

