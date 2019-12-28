# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:26:35 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicagoo
"""  
from osgeo import ogr

def shp2OsmosisPolygon(daShapefile,txtFn):        
    driver = ogr.GetDriverByName('ESRI Shapefile') 
    infile = driver.Open(daShapefile) 
    layer = infile.GetLayer()
    f= open(txtFn,"w") 
    f.write("osmosis polygon\nfirst_area\n")
    for area in layer: 
        area_shape = area.GetGeometryRef() 
        area_polygon = area_shape.GetGeometryRef(0) 
        no_of_polygon_vertices = area_polygon.GetPointCount()         
        for vertex in range(no_of_polygon_vertices): 
            lon, lat, z = area_polygon.GetPoint(vertex)  #获取经纬度坐标
            print(lon,lat,z)
            f.write("%s  %s\n"%(lon,lat))
    f.write("END\nEND")        
            
    f.close()      


if __name__=="__main__":
    daShapefile=r"D:\data\data_01_Chicago\QGisDat\OSMBoundary.shp"  
    txtFn=r"D:\data\data_01_Chicago\QGisDat\OSMBoundary.txt"
    shp2OsmosisPolygon(daShapefile,txtFn)


#Osmosis/Polygon Filter File Format example https://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Format#Converting_to.2Ffrom_POLY_format
#Here is an example of two polygon file (name: "australia_v") where the second polygon is a hole:
'''    
australia_v
first_area
     0.1446693E+03    -0.3826255E+02
     0.1446627E+03    -0.3825661E+02
     0.1446763E+03    -0.3824465E+02
     0.1446813E+03    -0.3824343E+02
     0.1446824E+03    -0.3824484E+02
     0.1446826E+03    -0.3825356E+02
     0.1446876E+03    -0.3825210E+02
     0.1446919E+03    -0.3824719E+02
     0.1447006E+03    -0.3824723E+02
     0.1447042E+03    -0.3825078E+02
     0.1446758E+03    -0.3826229E+02
     0.1446693E+03    -0.3826255E+02
END
second_area
     0.1422436E+03    -0.3839315E+02
     0.1422496E+03    -0.3839070E+02
     0.1422543E+03    -0.3839025E+02
     0.1422574E+03    -0.3839155E+02
     0.1422467E+03    -0.3840065E+02
     0.1422433E+03    -0.3840048E+02
     0.1422420E+03    -0.3839857E+02
     0.1422436E+03    -0.3839315E+02
END
END
''' 