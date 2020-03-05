# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:34:30 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import geopandas as gpd
import pandas as pd
import numpy as np



if __name__ == "__main__":
    censusBlocksFn=r"F:\data_02_Chicago\parkNetwork\Boundaries - Census Blocks - 2010.shp"
    populationCSVFn=r"F:\data_02_Chicago\parkNetwork\Population_by_2010_Census_Block.csv"
    censusBlocks=gpd.read_file(censusBlocksFn)    
    print(censusBlocks.columns)
    print(censusBlocks.dtypes)
    censusBlocks.geoid10=censusBlocks.geoid10.astype(np.float64)   
    
    
    population=pd.read_csv(populationCSVFn)
    print(population.columns)
    populaltionConcat=pd.concat([censusBlocks,population],keys=['geoid10','CENSUS BLOCK FULL'])
    merged_inner = pd.merge(left=censusBlocks, right=population, left_on='geoid10', right_on='CENSUS BLOCK FULL',sort=True)
    print(merged_inner.columns)

    populationCensusFn=r"F:\data_02_Chicago\parkNetwork\populationCensus.shp"
    merged_inner.to_file(populationCensusFn)