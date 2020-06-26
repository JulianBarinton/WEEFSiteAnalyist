'''
Commands to download different raster layers through earth engine.
Notice there is a dimension limit for some data providers e.g: 33554432 bytes for Copernicus
Image Collection:
To filter Image Collection according to date: filter(ee.Filter.date('2015-01-01', '2015-12-31'))
To get the most recent image from Image Collection: .sort('system:time_start', False).first()
To get the median value of all the selected layers: collection.reduce(ee.Reducer.median())
To select only the wanted layer: .select('name_of_layer'). The name_of_layer is reported in the website, and corresponds
 to the band name of the dataset

 #####For installation#######
In the terminal:
 #install the package
conda install -c conda-forge earthengine-api
 #authenticate
earthengine authenticate

'''
import ee
import geopandas as gpd
from Functions import download_url


##### Import layer with region boundaries and extract its extent#####
Area=gpd.read_file('Input/Namajavira_4326.shp')
minx, miny, maxx, maxy = Area.geometry.total_bounds
# Initialize the Earth Engine module.
ee.Initialize()


#########  DEM with 30m resoulution SRTM #########
# Get a download URL for an image.
image = ee.Image("USGS/SRTMGL1_003")
path = image.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)

download_url(path,'Output\Elevation.zip')

###########   Land cover ############
#Copernicus Global Land Cover Layers: CGLS-LC100 collection 2. 100m resolution. Ref year 2015
#download only image related to discrete classification (see in the documentation)
collection = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global").select('discrete_classification')
collection=collection.reduce(ee.Reducer.median()) #check other reducers

path = collection.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)

download_url(path,'Output\LandCoverCopernicus.zip')

# MCD12Q1.006 MODIS Land Cover Type Yearly Global 500m
collection = ee.ImageCollection("MODIS/006/MCD12Q1").select('LC_Prop1')#need to choose the best one and the wanted year

collection=collection.reduce(ee.Reducer.median())
path = collection.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)



#GlobCover: Global Land Cover Map. Year 2009. 300 m resoulution. year 2001-2016
image =ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3")
path = image.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)
download_url(path,'Output\LandCover.zip')
######## Climatic variables #############
#TerraClimate: Monthly Climate and Climatic Water Balance for Global Terrestrial Surfaces, University of Idaho. res 2.5 arcmin

image = ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE")

#WorldClim Climatology V1. Average from 1960 to 1991. Res=30 arc seconds. Mean, min, max temperature. Precipitation
image =ee.ImageCollection("WORLDCLIM/V1/MONTHLY")

#MOD16A2.006: Terra Net Evapotranspiration 8-Day Global 500m. kg/m^2/8day Derived by Penman Montheit. Value computed over 8 days period
image = ee.ImageCollection("MODIS/006/MOD16A2")

#WAPOR Actual Evapotranspiration and Interception. Value computed over 10 days period. 0.00223 arc degrees
ee.ImageCollection("FAO/WAPOR/2/L1_AETI_D")

######## Rivers #######
#HydroSHEDS layer, with accumulation and basins




########## Population #########
#worldpop. resolution=100m
collection = ee.ImageCollection("WorldPop/GP/100m/pop").sort('system:time_start', False)\
    .first().select('population')

path = collection.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)
download_url(path,'Output\Population.zip')

# GHSL: Global Human Settlement Layers, Population Grid 1975-1990-2000-2015 (P2016). 250 m resolution
collection=ee.ImageCollection("JRC/GHSL/P2016/POP_GPW_GLOBE_V1").sort('system:time_start', False)\
    .first().select('population_count')

path = collection.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)
download_url(path,'Output\Population.zip')

#GPWv411: Basic Demographic Characteristics (Gridded Population of the World Version 4.11). Data from census between 2000 and 2014.
#1 km resolution.
collection=ee.ImageCollection("CIESIN/GPWv411/GPW_Basic_Demographic_Characteristics").sort('system:time_start', False)\
    .first().select('basic_demographic_characteristics')

path = collection.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]
})
print(path)
download_url(path,'Output\PopulationCIESIN.zip')