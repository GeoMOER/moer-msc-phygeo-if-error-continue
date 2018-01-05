
import numpy
from osgeo import gdal


path = "C:/Users/tnauss/permanent/edu/msc-phygeo-if-error-continue/data/KB_DGM10/"
myArray  = numpy.loadtxt(path + "KB_DGM10.asc", skiprows=6)
myArray[1,1]