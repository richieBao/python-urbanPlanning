# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:58:43 2017

@author: RichieBao-caDesign设计(cadesign.cn)
"""
#百度地图POI数据采集,http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
#POI, http://lbsyun.baidu.com/index.php?title=lbscloud/poitags
from urllib.request import urlopen
from urllib import parse
import json
import csv
import conversionofCoordi as cc
import time

#conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='Lfyh0322',db='mysql',charset='utf8')
#cur=conn.cursor()
#cur.execute("USE scraping")
 
leftBottom=[108.776852,34.186027]
rightTop=[109.129275,34.382171]
partition=2
urlRoot='http://api.map.baidu.com/place/v2/search?' #行政区划区域检索:http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak=您的ak //GET请求
#urlRootDetail='http://api.map.baidu.com/place/v2/detail?' #地点详情检索服务:http://api.map.baidu.com/place/v2/detail?uid=5a8fb739999a70a54207c130&output=json&scope=2&ak=您的密钥 //GET请求
poiName='旅游景点'
AK='cXIfUp53G6GmH4dVFs4kyWaXy5I0sSVG'
fileName="baiduMapPoiSpotDetail.csv"
fileJsonName="baiduMapPoiSpotDetail.json"
#csvFile=open(fileName,'wt',encoding='utf-8')
csvFile=open(fileName,'w')
jsonFile=open(fileJsonName,'w')

def scrapingData(leftBottom,rightTop,partition,urlRoot,poiName,AK,csvFile):
    xDis=(rightTop[0]-leftBottom[0])/partition
    yDis=(rightTop[1]-leftBottom[1])/partition
    jsonDic=[]
    writer=csv.writer(csvFile)    
    num=0  
    for i in range(partition):
        for j in range(partition):
            leftBottomCoordi=[leftBottom[0]+i*xDis,leftBottom[1]+j*yDis]
            #rightTopCoordi=[rightTop[0]+i*xDis,rightTop[1]+j*yDis]
            rightTopCoordi=[leftBottom[0]+(i+1)*xDis,leftBottom[1]+(j+1)*yDis]
            #print(leftBottomCoordi,rightTopCoordi)
            for p in range(20):    
                query={
                   'query':poiName,
                   'page_size':'20', 
                   'page_num':str(p),
                   'scope':2,
                   'bounds':str(leftBottomCoordi[1]) + ',' + str(leftBottomCoordi[0]) + ','+str(rightTopCoordi[1]) + ',' + str(rightTopCoordi[0]),
                   'output':'json',
                   'ak':AK,                   
                }
                #url=urlRoot+'query=' + parse.urlencode(query) + '&page_size=20&page_num=' + str(p) + '&scope=1&bounds=' + str(leftBottomCoordi[1]) + ',' + str(leftBottomCoordi[0]) + ','+str(rightTopCoordi[1]) + ',' + str(rightTopCoordi[0]) + '&output=json&ak=' + AK;     
                url=urlRoot+parse.urlencode(query)
                #print(url)
                #time.sleep(1)
                data=urlopen(url)
#                print(data)
                responseJson=json.loads(data.read())                
                print(responseJson.get("message"))
                if responseJson.get("message")=='ok':
                    results=responseJson.get("results")     
                    #print(results)
                    csvRow=[]
                    for row in range(len(results)):  
                        subData=results[row]
                        orgiCoordi=[subData.get('location').get('lng'),subData.get('location').get('lat')]
                        converCoordiGCJ=cc.bd09togcj02(orgiCoordi[0], orgiCoordi[1])
                        converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
                        #csvRow=[subData.get('name'),subData.get('location').get('lat'),subData.get('location').get('lng'),subData.get('address')]
                        #csvRow=[subData.get('name'),subData.get('location').get('lat'),subData.get('location').get('lng'),subData.get('uid'),subData]
                        #print(csvRow)
                        #writer.writerow(csvRow)
                        writer.writerow([subData])
                        jsonDic.append(subData)

                        #jsonData=json.dumps([subData])
                        #jsonFile.write(jsonData)
                        
            num+=1
            print("第"+str(num)+"个区域写入csv/json文件")
    jsonData=json.dump(jsonDic,jsonFile)
    jsonFile.write('\n')
#cur.close()
#conn.close()
try:
    scrapingData(leftBottom,rightTop,partition,urlRoot,poiName,AK,csvFile)
finally:
    csvFile.close()
    jsonFile.close()