import time, random, requests
import DAN

import pandas as pd
import csv

ServerURL = 'https://5.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = "AACCDD112233" #if None, Reg_addr = MAC address

DAN.profile['dm_name']='11157039'
DAN.profile['df_list']=['receiveaccgyro']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line


#每0.1秒讀一次值，1秒，會跑10次
#data存畫一次圈/往下畫直線 的資料(資料格式是list還是dataframe?這裡我用dataframe)
#讓每10筆數值為一筆訓練資料
count=0
#trainDataCount=0 #count=10,trainDataCount+1
while True:
    try:
        # IDF_data = random.uniform(1, 10)
        # DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================
        
        ODF_data = DAN.pull('receiveaccgyro')#Pull data from an output device feature "Dummy_Control"
        #使用DictWriter
        file=open('daily.csv',mode='a',newline='')#加入newline，讓csv不會顯示一行空一行
        writer=csv.DictWriter(file,['acc1','acc2','acc3','pyro1','pyro2','pyro3'])

        if ODF_data != None:
            print("---------- count =",count)
            if(count%10==0):
                print("收集完第",count/10,"筆資料(每一筆資料含10行)")
            print(ODF_data[0],ODF_data[1],ODF_data[2],ODF_data[3],ODF_data[4],ODF_data[5])
            count=count+1
            writer.writerow({'acc1':ODF_data[0],'acc2':ODF_data[1],'acc3':ODF_data[2],'pyro1':ODF_data[3],'pyro2':ODF_data[4],'pyro3':ODF_data[5]})
            file.close()

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.1)  #每0.5秒 讀一次值

