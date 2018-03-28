a = [[10,13],[15,14]]
b = [15,14]
[b in a]
c = [ neu[i] not in kennichschon for i in range(len(neu))]

ar[48][88]
woist(0,1,ar)


#%%

import math
import gdal, ogr, osr, os
import numpy as np

# nach https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#replace-no-data-value-of-raster-with-new-value
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()


def maxprozeile(ar):
    for y in range(len(ar)):
        print(y, min(ar[y]))
        
def woist(wert, r, dmg_ar):
    for y in range(len(ar)):
        for x in range(len(ar[0])):
            if round(float(ar[y][x]), r) == wert:
                print("zeile:", y, "spalte:", x)
                return([y, x])

#%%
def canigo_fill(start, ar, fill):
    kennichschon=start[:]
    neu=start[:]
    startval=start[0]
    while len(neu) > 0:
        neu=[]
        for st in range(len(start)):
            for y in range(start[st][0]-1, start[st][0]+2):
                for x in range(start[st][1]-1, start[st][1]+2):
                    if ar[y][x] > ar[startval[0]][startval[1]]:
                        #print("groesseren Punkt gefunden")
                        return(True)
                    if ar[y][x] > fill:
                        neu.append((y,x))
                        neu = list(set(neu))
        start=[]
        for i in range(len(neu)):
            if neu[i] not in kennichschon:
                start.append((neu[i][0], neu[i][1]))
                start = list(set(start))
        kennichschon = kennichschon + start
        kennichschon = list(set(kennichschon))
        #print(len(neu), len(kennichschon), len(start))
    else:
        #print("kein weiterer Gipfel")
        return(False)        



#%%
#################################################################################
for y in range(len(ar)):
    for x in range(len(ar[0])):
        if ar[y][x] == 0:
            print(ar[y][x], y, x)





ar = raster2array("/home/hannes/Dokumente/UniMR/py/test.tif")
ar2 = raster2array("/home/hannes/Dokumente/UniMR/py/testkeingipfel.tif")

canigo( start, ar2, gl)

#################################################################################      
gl=[[50,350], [80,50]]
start=[[80,50]]    
#%%
def prominenz(start, ar, gl, dwn_stp):
    fillv = ar[start[0][0]][start[0][1]]
    gipfel = False
    while gipfel == False:
        gipfel = canigo_fill(start, ar, fillv-dwn_stp)
        fillv = fillv - dwn_stp
    return(fillv)


#%%
gl=[[78,60]]

start = [[113,128]]

ar = raster2array("D:/UniData/py/subalpen.tif")   

def woist(wert, r, dmg_ar):
    for y in range(len(ar)):
        for x in range(len(ar[0])):
            if round(float(ar[y][x]), r) == wert:
                print("zeile:", y, "spalte:", x)
                return([y, x])

#%%
woist(2215.198, 3, ar)  
#%%   
prominenz(start, ar, gl, 10)    
    

