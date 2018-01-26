
#%%
import math
import gdal
import ogr
import osr
import os
import numpy as np
# props an https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#replace-no-data-value-of-raster-with-new-value
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()

#%%
dgm = gdal.Open(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")
#%%
ar = raster2array(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")
#%%
#gipfelsuche entweder im gis oder hiermit
for y in range(len(ar)):
    print(y, max(ar[y]))
#%%
#vermeintliche gipfelhoehe als zahl eingeben
#dateityp des arrays (float32) ist anders als float (2041.27 z.B.), logische abfragen in py daher immer FALSE
for y in range(len(ar)):
    if round(float(max(ar[y])), 2) == 2041.27 :
        print(y, max(ar[y]))
        for x in range(len(ar[0])):
            if round(float(ar[y][x]), 2) == 2041.27:
                print("zeile:", y, "spalte:", x)
    
#%%
#nur so
dgm = gdal.Open(r"C:\Users\tnauss\permanent\edu\msc_2017\classroom-2017\python\msc-phygeo-class-of-2017-schnell7-1\Python\ws09\subalpen.tif")

#%%
#z,s, gipfelkoordinaten, y,x von dominanz()
def distanz(z,s,y,x):
    dis = math.sqrt((z-y)**2 + (s-x)**2)    
    return(dis)

#zeile, spalte(des gipfels), array des dgm, step grosse des fensters minimale dis wird ausgesucht, res = zellengroesse
def dominanz(z,s, dgm_ar, step, res):
    end_list = []
    di = 1
    for y in range(z-step, z+step+1):
        for x in range(s-step, s+step+1):
            if dgm_ar[z][s] < dgm_ar[y][x]:
                dissi = distanz(z,s,y,x)
                end_list.append(dissi)
                
    if len(end_list)> 0:
        print(end_list)
        return(min(end_list)*res)
    else:
        print("""Alarm!Alarm!Alarm!Alarm!Alarm!Alarm! \n\n       setze 'step' groesser!\n\n====================================""")
        

        
        
#%%


#%%
dominanz(80,65,ar,64,200)
    
#%%
def eigenstand(h, d, p):
  if d < 100000:
    E1 = math.log(h/8848, 2) + math.log(d/100000, 2) + math.log(p/h, 2)
    E = -(E1/3)
  else:
    E1 = math.log(h/8848, 2) + math.log((p/h), 2)
    E = -(E1/3)
  return(E)  
  
#%%
 #300 wird hier yum test angenommen
 #gipfel hat nahegelegen hoeheren gipfelnachbar deswegen reicht 5 (3 ginge auch)
h = float(ar[78][60])
d = dominanz(78,60,ar,5,200)
eigenstand(h, 300, d)
#%%
#naechster hoeherer gipfel viel wieter weg; 
h2 = float(ar[80][65])
d2 = dominanz(80,65,ar,64,200)
eigenstand(h2, 300, d2)

#%%
#der Ansatz, das Fenster schrittweise zu vergroessern ist nicht ideal:
#liegt der erste Punkt > Gipfel in der diagonalen des Quadrats ist die Entfernung
#e = x*(wurzel 2)
#ein wesentlich groessere Fenster kann aber trotzdem einen naeheren Punkt enthalten
#(wenn nur in x bzw y Richtung gegangen wird)
#Bsp fenstergroesse 50
distanz(0,0,50,50)
# = 70,71
#also ein fenster der groesse 70 kann eine naehere distanz (70<70,71) haben
distanz(0,0,0,70)
# = 70
#bsp von werten fuer 80\65
#14990.663761154807 53 / erster treffer
#13172.69904006009 60
#12801.562404644206 64
#12801.562404644206 100
#12801.562404644206 125 /letzter treffer weil .tif zu klein
#Erkenntnis: das Fenster sollte eher die maximale Ausdehnung oder zumindest eine sehr grosse haben
#oder die groesse erhoeht sich um xneu = xalt * (wurzel 2) auf die naechste ganzzahl aufgerundet
#beim Beispiel von 50 also auf 71
