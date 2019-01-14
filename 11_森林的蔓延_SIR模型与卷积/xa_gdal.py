# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:27:03 2017

@author:richieBao-caDesign设计(cadesign.cn)
"""
import gdal,ogr,os,osr,gdalnumeric
import sys
import ospybook as pb
from ospybook.vectorplotter import VectorPlotter 
import numpy as np

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码

fn=r'E:\MUBENAcademy\pythonSystem\dataA' 

'''获取元数据metadata'''
def gettingMetadata(fn,lyrName):
    ds=ogr.Open(fn,0)
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    lyr=ds.GetLayer(lyrName)    
    print("extent:",lyr.GetExtent()) #(min_x,max_x, min_y, max_y)
    print("GeomType:",lyr.GetGeomType(),"wkbPoint?",lyr.GetGeomType()==ogr.wkbPoint) #返回索引，根据索引查找对应的数据类型
    feat=lyr.GetFeature(0)
    print("GeomTypeByfeature:",feat.geometry().GetGeometryName())
    print("spatialRef:",lyr.GetSpatialRef())  #空间坐标
    print("fieldAttri:",[(field.name,field.GetTypeName()) for field in lyr.schema])
    lyrName=lyrName+".shp"
    pb.print_attributes(os.path.join(fn,lyrName), 3, ["NAME","KIND"])

'''point的读与可视化'''
def pointReading(fn,pt_lyrName_r):
    ds=ogr.Open(fn,0) #0为只读模式，1为编辑模式
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    pt_lyr=ds.GetLayer(pt_lyrName_r) #可以直接数据层(文件)名或者指定索引
    vp = VectorPlotter(True)  #显示vector数据
    vp.plot(pt_lyr,'bo')
    
    i=0
    for feat in pt_lyr: #循环feature
        pt=feat.geometry()
        pt_x=pt.GetX()
        pt_y=pt.GetY()
        name=feat.GetField('NAME')
        kind=feat.GetField('KIND')
        print(name,kind,(pt_x,pt_y,))
        i+=1
        if i==12:
            break
    del ds

'''可以将建立datasource数据源单独定义函数，方便调用'''

'''point的写入'''
def pointWriting(fn,pt_lyrName_w,ref_lyr=False):
    ds=ogr.Open(fn,1)
    
    '''参考层，用于空间坐标投影，字段属性等参照'''
    ref_lyr=ds.GetLayer(ref_lyr)
    ref_sr=ref_lyr.GetSpatialRef()
    print(ref_sr)
    ref_schema=ref_lyr.schema #查看属性表字段名和类型
    for field in ref_schema:
        print(field.name,field.GetTypeName())   
 
    '''建立新的datasource数据源'''
    sf_driver=ogr.GetDriverByName('ESRI Shapefile')
    sfDS=os.path.join(fn,r'sf')
    if os.path.exists(sfDS):
        sf_driver.DeleteDataSource(sfDS)
    pt_ds=sf_driver.CreateDataSource(sfDS)
    if pt_ds is None:
        sys.exit('Could not open{0}'.format(sfDS))
        
    '''建立新layer层'''    
    if pt_ds.GetLayer(pt_lyrName_w):
        pt_ds.DeleteLayer(pt_lyrName_w)    
    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,ref_sr,ogr.wkbPoint)
    
    '''配置字段，名称以及类型和相关参数'''
    pt_lyr.CreateFields(ref_schema)
    LatFd=ogr.FieldDefn("origiLat",ogr.OFTReal)
    LatFd.SetWidth(8)
    LatFd.SetPrecision(3)
    pt_lyr.CreateField(LatFd)
    LatFd.SetName("Lat")
    pt_lyr.CreateField(LatFd)
     
    '''建立feature空特征和设置geometry几何类型'''
    print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
    
    for feat in ref_lyr:  #循环feature
        '''设置几何体'''
        pt_ref=feat.geometry().Clone()
        wkt="POINT(%f %f)" %  (float(pt_ref.GetX()+0.01) , float(pt_ref.GetY()+0.01))
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
        for i_field in range(feat.GetFieldCount()):
            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",pt_ref.GetX())
        pt_feat.SetField("Lat",pt_ref.GetX()+0.01)
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds

'''line的读和可视化'''
def lineReading(fn,ln_lyrName_r):    
    ds=ogr.Open(fn,0) #0为只读模式，1为编辑模式
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    ln_lyr=ds.GetLayer(ln_lyrName_r) #可以直接数据层(文件)名或者指定索引
    
    vp = VectorPlotter(True) #显示vector数据
    vp.plot(ln_lyr,'bo')
    
    ln_schema=ln_lyr.schema #查看属性表字段名和类型
    for field in ln_schema:
        print(field.name,field.GetTypeName())     
        
    i=0    
    for feat in ln_lyr: #循环feature
        ln=feat.geometry() #获取feature的几何对象
        name=feat.GetField('name')  #读取feature的属性
        Shape_Leng=feat.GetField('Shape_Leng')
        print(name,Shape_Leng,'\n',ln,'\n',ln.GetPointCount())        
        for j in range(ln.GetPointCount()):  #循环几何对象(线)d的vertex顶点
            if j<6:
                print((i,ln.GetX(i),ln.GetY(i))) #只能通过GetX()和GetY()的方法获取顶点坐标
        i+=1
        if i==12:
            break
    del ds    
 
'''line的写入'''
def lineWriting(fn,ln_lyrName_w,ref_lyr=False):
    ds=ogr.Open(fn,1)
    
    '''参考层，用于空间坐标投影，字段属性等参照'''
    ref_lyr=ds.GetLayer(ref_lyr)
    ref_sr=ref_lyr.GetSpatialRef()
    print(ref_sr)
    ref_schema=ref_lyr.schema #查看属性表字段名和类型
    for field in ref_schema:
        print(field.name,field.GetTypeName())      

    '''建立新layer层'''    
    if ds.GetLayer(ln_lyrName_w):
        ds.DeleteLayer(ln_lyrName_w)    
    ln_lyr=ds.CreateLayer(ln_lyrName_w,ref_sr,ogr.wkbMultiLineString)    

    '''配置字段，名称以及类型和相关参数'''
    Fd=ogr.FieldDefn("length",ogr.OFTReal)
    Fd.SetWidth(8)
    Fd.SetPrecision(3)
    ln_lyr.CreateField(Fd)
    Fd=ogr.FieldDefn("name",ogr.OFTString)
    ln_lyr.CreateField(Fd)    

    '''建立feature空特征和设置geometry几何类型'''
    print(ln_lyr.GetLayerDefn())
    ln_feat=ogr.Feature(ln_lyr.GetLayerDefn())

    for feat in ref_lyr:  #循环feature
        '''设置几何体'''
        ln_ref=feat.geometry().Clone()
        temp=""
        for j in range(ln_ref.GetPointCount()):
            if j==ln_ref.GetPointCount()-1:
                temp+="%f %f"%(float(ln_ref.GetX(j)+0.01) , float(ln_ref.GetY(j)+0.01))
            else:
                temp+="%f %f,"%(float(ln_ref.GetX(j)+0.01) , float(ln_ref.GetY(j)+0.01))
        wkt="LINESTRING(%s)" % temp  #使用wkt的方法建立直线
#        print(wkt)
        newLn=ogr.CreateGeometryFromWkt(wkt)        
        ln_feat.SetGeometry(newLn)
        '''设置字段值'''
        ln_feat.SetField("name",feat.GetField("name"))
        ln_feat.SetField("length",newLn.Length())
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        ln_lyr.CreateFeature(ln_feat)    
    del ds

'''polygon的读和可视化'''
def polygonReading(fn,pg_lyrName_r):    
    ds=ogr.Open(fn,0) #0为只读模式，1为编辑模式
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    pg_lyr=ds.GetLayer(pg_lyrName_r) #可以直接数据层(文件)名或者指定索引
    
    vp = VectorPlotter(True) #显示vector数据
    vp.plot(pg_lyr)
    
    pg_schema=pg_lyr.schema #查看属性表字段名和类型
    for field in pg_schema:
        print(field.name,field.GetTypeName())     
        
    i=0    
    for feat in pg_lyr: #循环feature
        print("..................................................................")
        atts=feat.items()
        print(atts)
        pg=feat.geometry() #获取feature的几何对象
#        ring=
        name=feat.GetField('NAME')  #读取feature的属性
        Shape_Area=feat.GetField('Shape_Area')
        print(name,Shape_Area,'\n',pg,'\n')   
        
        for j in range(pg.GetGeometryCount()):  #循环几何对象获取ring,获取顶点坐标
            ring=pg.GetGeometryRef(j)
            for coordi in ring.GetPoints():
                print(coordi)
        i+=1
        if i==12:
            break
    del ds 

'''polygon的写入'''
def polygonWriting(fn,pg_lyrName_w,ref_lyr=False):
    ds=ogr.Open(fn,1)
    
    '''参考层，用于空间坐标投影，字段属性等参照'''
    ref_lyr=ds.GetLayer(ref_lyr)
    ref_sr=ref_lyr.GetSpatialRef()
#    print(ref_sr)
    ref_schema=ref_lyr.schema #查看属性表字段名和类型
    for field in ref_schema:
        print(field.name,field.GetTypeName())      

    '''建立新layer层'''    
    if ds.GetLayer(pg_lyrName_w):
        ds.DeleteLayer(pg_lyrName_w)    
    pg_lyr=ds.CreateLayer(pg_lyrName_w,ref_sr,ogr.wkbMultiPolygon)    

    '''配置字段，名称以及类型和相关参数'''
    Fd=ogr.FieldDefn("area",ogr.OFTReal)
    Fd.SetWidth(8)
    Fd.SetPrecision(8)
    pg_lyr.CreateField(Fd)
    Fd=ogr.FieldDefn("name",ogr.OFTString)
    pg_lyr.CreateField(Fd)    

    '''建立feature空特征和设置geometry几何类型'''
#    print(pg_lyr.GetLayerDefn())
    pg_feat=ogr.Feature(pg_lyr.GetLayerDefn())
    
    for feat in ref_lyr:  #循环feature
        '''设置几何体'''
        pg_ref=feat.geometry().Clone()
        tempSub=""
        for j in range(pg_ref.GetGeometryCount()):
            ring=pg_ref.GetGeometryRef(j)
            vertexes=ring.GetPoints()
#            print(len(vertexes))
            temp=""
            for i in range(len(vertexes)):                
                if i==len(vertexes)-1:
                    temp+="%f %f"%(float(vertexes[i][0]+0.01) , float(vertexes[i][1]+0.01))
                else:
                    temp+="%f %f,"%(float(vertexes[i][0]+0.01) , float(vertexes[i][1]+0.01))
            if j==pg_ref.GetGeometryCount()-1:
                tempSub+="(%s)"%temp   
            else:
                tempSub+="(%s),"%temp
#        print(tempSub)    
        wkt="POLYGON(%s)" % tempSub  #使用wkt的方法建立直线
#        print(wkt)
        newPg=ogr.CreateGeometryFromWkt(wkt)        
        pg_feat.SetGeometry(newPg)
        
        '''设置字段值'''
        pg_feat.SetField("name",feat.GetField("NAME"))
        pg_feat.SetField("area",newPg.GetArea())
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pg_lyr.CreateFeature(pg_feat)    
    del ds

'''raster栅格数据的读写'''
def rasterRW(fn,raster_lyr,raster_lyr_w):
    gdal.UseExceptions()
    
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(os.path.join(fn,raster_lyr))
    except RuntimeError as e:
        print( 'Unable to open %s'% os.path.join(fn,raster_lyr))
        print(e)
        sys.exit(1)
    print("metadata:",src_ds.GetMetadata())   
    
    '''获取所有波段'''
    srcband=[]
    for band_num in range(1,5):
        try:
            srcband.append(src_ds.GetRasterBand(band_num))
        except RuntimeError as e:
            print('Band ( %i ) not found' % band_num)
            print(e)
            sys.exit(1)
    print(srcband)
    
    '''获取用于NDVI计算的红和近红波段数组,并计算ndvi'''
    red=srcband[0].ReadAsArray().astype(np.float)
    nir=srcband[3].ReadAsArray()
    red=np.ma.masked_where(nir+red==0,red)
    ndvi=(nir-red)/(nir+red)
    ndvi=ndvi.filled(-99)
    print(ndvi.shape,ndvi.std())
    
    '''初始化输出栅格'''
    driver=gdal.GetDriverByName('GTiff')
    out_raster=driver.Create(os.path.join(fn,raster_lyr_w),src_ds.RasterXSize,src_ds.RasterYSize,1,gdal.GDT_Float64)
    out_raster.SetProjection(src_ds.GetProjection()) #设置投影与参考栅格同
    out_raster.SetGeoTransform(src_ds.GetGeoTransform()) #配置地理转换与参考栅格同
    
    '''将数组传给栅格波段，为栅格值'''
    out_band=out_raster.GetRasterBand(1)
    out_band.WriteArray(ndvi)
    
    '''设置overview'''
    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    out_raster.BuildOverviews('average', overviews)
    
    '''清理缓存与移除数据源'''
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    del src_ds,out_raster,out_band

if __name__=="__main__":
    pt_lyrName_r=r'xa_tourism'
    pointReading(fn,pt_lyrName_r)
#    pt_lyrName_w='xa_tourism_w'
#    pointWriting(fn,pt_lyrName_w,ref_lyr=pt_lyrName_r)
#    gettingMetadata(fn,pt_lyrName_r)
#    ln_lyrName_r=r'xa_metroline'
#    ln_lyrName_w='xa_metroline_w'
#    lineReading(fn,ln_lyrName_r)
#    fn_ln=r'D:\MUBENAcademy\pythonSystem\dataA\sf' 
#    lineWriting(fn,ln_lyrName_w,ref_lyr=ln_lyrName_r)
#    pg_lyrName_r=r'xianGreenspace'
#    pg_lyrName_w=r'xianGreenspace_w'
#    polygonReading(fn,pg_lyrName_r)
#    polygonWriting(fn,pg_lyrName_w,ref_lyr=pg_lyrName_r)
#    raster_lyr=(r'LC81270362017107LGN00_B2.TIF',r'LC81270362017107LGN00_B3.TIF',r'LC81270362017107LGN00_B4.TIF')    
#    raster_lyr=r'xaGFCm.tif'
#    raster_lyr_w=r'xaNDVI.tif'
#    rasterRW(fn,raster_lyr,raster_lyr_w)