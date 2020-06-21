# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:12:28 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""
import driverlessCityProject_spatialPointsPattern_association_basic as basic
import pandas as pd
import os







if __name__ == "__main__":
    #merge data together
    dataPath=[
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_PHMI.fig" },
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_PHMI.fig"},
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\PHMI.fig"},
        # {"landmark":,
        #  "phmi":  },
        ]   
    i=0
    for dat in dataPath:
        landmarks_fn=dat["landmark"]
        phmi_fn=dat["phmi"]
        #01   
        LandmarkMap_dic=basic.readMatLabFig_LandmarkMap(landmarks_fn)
        try:
            PHMI_dic=basic.readMatLabFig_PHMI_A(phmi_fn,LandmarkMap_dic)
            print("applied type -A")
        except:
            PHMI_dic=basic.readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
            print("applied type -B")    
        #-01    
        Phmi=PHMI_dic[1][2]         
        #-03
        PHMIList=PHMI_dic[1][2].tolist()
        
        landmarks_coordi=LandmarkMap_dic[1]
        PHMI_coordi=PHMI_dic[0]

    landmarks_df=pd.DataFrame(data=np.array(landmarks_coordi).T, columns=["landmark_x", "landmark_y",])
    location_df=pd.DataFrame(np.array(PHMI_coordi[:2]).T,columns=["location_x","location_y"])
    phmi_df=pd.DataFrame(data=Phmi,columns=["phmi"])
    
    #configure save path 配置保存路径
    data_root=r"C:\Users\richi\omen-richiebao\omen-grasshopper"
    landmarks_df.to_csv(os.path.join(data_root,"landmarks.csv"),index=False)  
    location_df.to_csv(os.path.join(data_root,"location.csv"),index=False)  
    
    phmi_df.to_csv(os.path.join(data_root,"phmi.csv"),index=False)  
    