#1.先把10筆資料串成一行最後加上label的數字(circle:1,line:2,daily:3)
#2.合併三個csv檔->combine.csv


import csv


rowInTen=[]#存一列60筆數值
datas=[]#存100筆rowInTen
count=0
with open('daily.csv') as file:
    data=csv.reader(file)#使用csv.reader讀出來的的資料是list
    for row in data:
        #每10比換一行
        if count%10==0 and count!=0:    
            datas.append(rowInTen)   #append是加到下一列   先把之前rowInTen的資料append到datas  append前面不須賦值
            rowInTen=[] #再把rowInTen清空
            rowInTen=rowInTen+row        
            count+=1
        else:
            rowInTen=rowInTen+row   #這樣寫是list串接
            count+=1

#print(type(datas))#list
print(len(datas))
#寫檔combine.csv
for i in datas:
    #開啟輸出的 CSV 檔案
    with open('combine.csv','a',newline='') as csvfile:
        #建立 CSV 檔寫入器
        writer=csv.writer(csvfile)
        #寫入一列資料
        writer.writerow(i)



# rows=[]
# file=open('circle.csv')
# reader=csv.DictReader(file,['acc1','acc2','acc3','pyro1','pyro2','pyro3'])#這是csv沒有標題的寫法
# for row in reader:
#     print(row['acc1'],row['acc2'],row['acc3'],row['pyro1'],row['pyro2'],row['pyro3'])
