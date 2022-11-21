import time, random,requests
import DAN

import numpy as np
import pandas as pd
#載入已訓練好的模型來做預測
from joblib import load

ServerURL = 'https://5.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = "AACCDD112B3A" #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control',]
DAN.profile['d_name']= 'Dummy_Device_11157039' # Assign a Device Name
# DAN.profile['is_sim']= True
DAN.state='RESUME'

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

#載入模型
decisionTreeModel=load('decision_tree_model')

#模型function  沒寫完  學長寫的function code還沒了解state...
def ml_predict(inputData):
    
    result=decisionTreeModel.predict(inputData)
    return result



#一個動作需要一秒鐘，因為每0.1秒就會收集一次資料所以會收集10次，共60筆 
count=1
oneData=[]
datalist=[]

light=0.5

while True:
    try:
        # IDF_data = random.uniform(1, 10)
        # DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================   
        ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        
        if ODF_data != None:
            if count % 10 != 0 and count !=0:
                print("正在收集",count,"/10資料")
                oneData=[ODF_data[0][0],ODF_data[0][1],ODF_data[0][2],ODF_data[0][3],ODF_data[0][4],ODF_data[0][5]]
                datalist.append(oneData)
                count+=1
            else:
                oneData=[ODF_data[0][0],ODF_data[0][1],ODF_data[0][2],ODF_data[0][3],ODF_data[0][4],ODF_data[0][5]]
                datalist.append(oneData)
                print("收集完一筆資料(60組數值)--------------------")
                #print(datalist)
                count=1
                oneData=[]
                
                #一定要加這一行 reshape把資料變成一格陣列
                datalist=pd.DataFrame(np.array(datalist).reshape(1,-1),columns=['acc11','acc21','acc31','pyro11','pyro21','pyro31','acc12','acc22','acc32','pyro12','pyro22','pyro32','acc13','acc23','acc33','pyro13','pyro23','pyro33','acc14','acc24','acc34','pyro14','pyro24','pyro34','acc15','acc25','acc35','pyro15','pyro25','pyro35','acc16','acc26','acc36','pyro16','pyro26','pyro36','acc17','acc27','acc37','pyro17','pyro27','pyro37','acc18','acc28','acc38','pyro18','pyro28','pyro38','acc19','acc29','acc39','pyro19','pyro29','pyro39','acc110','acc210','acc310','pyro110','pyro210','pyro310'])
                #用模型判斷
                predictResult=ml_predict(datalist)  #可能這裡的datalist要在處理一下轉成model可以訓練一筆的格式
                #print(predictResult)
                print("-----手勢偵測結果-----")
                if predictResult==1:
                    print("偵測到畫圈，燈泡亮度變 1\n")
                    light=1
                elif predictResult==2:    
                    print("偵測到往上再往下，燈泡亮度變 0\n")
                    light=0
                else:
                    print("沒有偵測到手勢，燈泡亮度變0.5\n")
                    light=0.5

                datalist=[]
                print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")
                DAN.push ('Dummy_Sensor', light) #Push data to an input device feature "Dummy_Sensor"

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    #每0.1s秒 讀一次值
    time.sleep(0.1)  

