import time, random, requests
import DAN

ServerURL = 'https://5.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = "AACCDD112233" #if None, Reg_addr = MAC address

DAN.profile['dm_name']='11157039'
DAN.profile['df_list']=['receiveaccgyro']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

while True:
    try:
        # IDF_data = random.uniform(1, 10)
        # DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================

        ODF_data = DAN.pull('receiveaccgyro')#Pull data from an output device feature "Dummy_Control"
        if ODF_data != None:
            print("----------")
            print(ODF_data[0])
            print(ODF_data[1])
            print(ODF_data[2])
            print(ODF_data[3])
            print(ODF_data[4])
            print(ODF_data[5])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)  #每0.2秒 讀一次值

