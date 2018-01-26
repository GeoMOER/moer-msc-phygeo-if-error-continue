#!/usr/bin/env python
'''
import qgis
from qgis.core import *
import sys

app = QgsApplication([],True, None)
app.setPrefixPath("/usr", True)
app.initQgis()
sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

print Processing.getAlgorithm("qgis:creategrid")
print Processing.getAlgorithm("saga:ordinarykriging")




Created on 04.01.2018

@author: tnauss
'''
'''
os.environ['GISBASE'] = r'C:\OSGeo4W64\apps\grass\grass-7.2.2'
os.environ['LD_LIBRARY_PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\lib'
os.environ['PATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\;C:\OSGeo4W64\bin'
os.environ['PYTHONLIB']= r'C:\OSGeo4W64\apps\Python27'
os.environ['PYTHONPATH']= r'C:\OSGeo4W64\apps\grass\grass-7.2.2\etc\python;C:\OSGeo4W64\apps\qgis\python'
'''

import sys
import os
import grass.script as grass
import grass.script.setup as gsetup
import qgis
from qgis.core import *
from osgeo import ogr
from osgeo import gdal
from PyQt4.QtCore import QFile, QFileInfo

qgs = QgsApplication([],True, None)
#qgs.setPrefixPath("/usr", True)
qgs.initQgis()
print(QgsApplication.showSettings()) 


from processing.core.Processing import Processing
from processing.tools import *
Processing.initialize()

print Processing.getAlgorithm("qgis:creategrid")
print Processing.getAlgorithm("grass:r.to.vect")

''' Define datapath
'''
datapath = r"C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue\data"
dgmpath = datapath + os.sep + "KU_DGM10\KU_DGM10.tif"
gipfelpath = datapath + os.sep + r"gipfelliste\brandenberger_alpen.shp"
tmppath = datapath + os.sep + r"temp"


''' Read geo files
'''
# Summit list
s = QgsVectorLayer(gipfelpath, "gipfel", "ogr")
print(s.isValid())
s.crs().toProj4()
s.extent().asWktCoordinates()

# DGM
dgm= QgsRasterLayer(dgmpath, QFileInfo(dgmpath).baseName())
print(dgm.isValid())
dgm.crs().toProj4()
dgm.extent().asWktCoordinates()

# Raster to point conversion
xmin = dgm.extent().xMinimum()
xmax = dgm.extent().xMaximum()
ymin = dgm.extent().yMinimum()
ymax = dgm.extent().yMaximum()
dgmext = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)

''' Compute values
'''
# for f in s.getFeatures():
#     print f.attributes()
#     g = f.geometry()
# Dummy for first feature; has to be included in iteration over all summits later.
f = s.getFeatures().next()
g = f.geometry()

# Get summit height
hs= dgm.dataProvider().identify(g.centroid().asPoint(), QgsRaster.IdentifyFormatValue)
if hs.isValid():
    print hs.results()

# Write reclass file
rfile = tmppath + os.sep + "temp.txt"
with open(rfile, "w") as text_file:
    text_file.write("%s thru 99999999999999999 = 1" % hs.results()[1])
general.runalg("grass7:r.reclass", dgm, None, "%s thru 99999999999999999 = 1" % hs.results()[1], dgmext, 1, tmppath + os.sep + "test.tif")
general.runalg("grass7:r.info", dgm, True, True, True, True, False, False, False, False, False, dgmext, tmppath + os.sep + "test.html", tmppath + os.sep + "test.txt")
general.alghelp("grass7:r.reclass")





#general.runalg("grass7:r.to.vect", dgm, 1, False, "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax), 1, datapath + os.sep + "test.shp")
general.alghelp("grass7:r.reclass", dgm, )

#r.distance
#r.reclass


''' Compute values
'''
# for f in s.getFeatures():
#     print f.attributes()
#     g = f.geometry()
# Dummy for first feature; has to be included in iteration over all summits later.
f = s.getFeatures().next()
g = f.geometry()

# Get summit height
hs= dgm.dataProvider().identify(g.centroid().asPoint(), QgsRaster.IdentifyFormatValue)
if hs.isValid():
    print hs.results()
    
    
    
# Comput distance
point1 = QgsPoint(-46.443077,-67.51561)
point2 = QgsPoint(-46.4446,-67.512778)

point1 = QgsPoint(129926,269342)
point1 = QgsPoint(129921,269342)
#distance.measureLine(g.centroid().asPoint(), g.centroid().asPoint())
#Create a measure object
distance = QgsDistanceArea()
crs = QgsCoordinateReferenceSystem()
#crs.createFromSrsId(3452) # EPSG:4326
crs.createFromUserInput("EPSG:31254")
distance.setSourceCrs(crs)
distance.setEllipsoidalMode(False)
distance.setEllipsoid('WGS84')
m = distance.measureLine(point1, point2)
print(m)