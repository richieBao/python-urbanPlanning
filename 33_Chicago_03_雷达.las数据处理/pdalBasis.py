# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:04:39 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import pdal
fn=r"D:/data/lidar/lidar_bundle/06_river forest/LAS_11009275.las" #pdal目前只识别左斜杠"/"
json = """
{
  "pipeline": [
    "%s",
    {
        "type": "filters.sort",
        "dimension": "X"
    }
  ]
}"""%fn


pipeline = pdal.Pipeline(json)
pipeline.validate() # check if our JSON and options were good
pipeline.loglevel = 8 #really noisy
count = pipeline.execute()
arrays = pipeline.arrays
metadata = pipeline.metadata
print("+"*50)
print(metadata)
log = pipeline.log