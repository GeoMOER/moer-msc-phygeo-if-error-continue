'''
Created on 04.01.2018

@author: tnauss
'''
import sys
import os

'''
os.environ['GISBASE'] = r'C:\OSGeo4W64\apps\grass\grass-7.2.2'
os.environ['LD_LIBRARY_PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\lib'
os.environ['PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\;C:\OSGeo4W64\bin'
os.environ['PYTHONLIB']= r'C:\OSGeo4W64\apps\Python27'
os.environ['PYTHONPATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\etc\python;C:\OSGeo4W64\apps\qgis\python'
'''

import grass.script as grass
import grass.script.setup as gsetup
from qgis.core import *
from osgeo import ogr

datapath = r"C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue\data\gipfelliste\bergliste-komplett.kmz"
dataSource = ogr.Open(datapath)
layer = dataSource.GetLayer()
layer_defn = layer.GetLayerDefn()
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
for feature in layer:
    print feature.GetField("Name")
layer.ResetReading()

'''
gisdb = os.path.join(os.getenv('APPDATA', grassdata'))m6+n
  1 45 80m8m,///n/j//mmm8//m/12222jmnjm*n+
gisbase = os.environ['GISBASE'] 
gisdbase = os.path.join(r'C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue\grass')
location = "Kufstein"
mapset   = "PERMANENT"

gsetup.init(gisbase, gisdbase, location, mapset)

grass.message('--- GRASS GIS 7: Current GRASS GIS 7 environment:')
print grass.gisenv()

grass.message('--- GRASS GIS 7: Checking projection info:')
in_proj = grass.read_command('g.proj', flags = 'jf')
kv = grass.parse_key_val(in_proj)
print kv
print kv['+proj']

grass.message('--- GRASS GIS 7: Checking computational region info:')
in_region = grass.region()
grass.message("--- Computational region: '%s'" % in_region)

grass.run_command("g.list", type="raster")
grass.run_command("r.contour", input="KU_DGM10", output="kontur", step=10, minlevel=0, maxlevel=3000, overwrite = True)

grass.run_command("g.list", type="vector")
grass.run_command("v.out.ogr", overwrite=True, input="kontur", output=r"C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue\data\kontur", format="ESRI_Shapefile")



location_path = os.path.join(gisdb, location)
# print 'Removing location %s' % location_path
# shutil.rmtree(location_path)

# sys.exit(0)
'''
