# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:57:55 2016

@author: jiahu_000
"""

#模块装载
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#从excel读取数据
data = xlrd.open_workbook('dataday.xlsx')
table = data.sheets()[0] 
date=table.col_values(0) #交易日期
date=date[3:]
if00=table.col_values(5) #当月合约收盘价
if00=if00[3:]
if01=table.col_values(18) #下月合约收盘价
if01=if01[3:]

#价差分析画图
gap=[x-y for x,y in zip(if00,if01)]
fig1 = plt.figure(1,figsize=(12,6))
plt.subplot(221)
plt.plot_date(date,if00,'b-')
plt.title('IF00')
plt.subplot(222)
plt.plot_date(date,if01,'b-')
plt.title('IF01')
plt.subplot(212)
plt.plot_date(date,gap,'b-')
plt.title('IF00-IF01') 
fig2 = plt.figure(2,figsize=(12,6))
plt.hist(gap)
plt.title('gap_frequency')

#价差布林轨道线
times=3 #几倍标准差
t_p=20 #n天的移动平均
initial= np.empty((4,len(if01),))
initial[:] = np.NAN
initial[0]=gap
initial=initial.T
boll=pd.DataFrame(initial,columns=["gap","mean","upline","downline"])
boll['mean']=pd.rolling_mean(boll['gap'],t_p) #价差均线
boll['upline']=pd.rolling_mean(boll['gap'],t_p)+times*pd.rolling_std(boll['gap'],t_p) #上限
boll['downline']=pd.rolling_mean(boll['gap'],t_p)-times*pd.rolling_std(boll['gap'],t_p) #下限
fig3=plt.figure(3,figsize=(12,6))
plt.plot(boll)
plt.title('bolling')

#回测
#开仓逻辑：价差上穿上限，赌价差收敛，空IF00空IF01/价差下穿下限，赌价差扩大，多IF00空IF01
#平仓逻辑：价差从上限回落下穿均线，价差从下限上穿均线
n_w=[]
position=0
le=2 #杠杆
for i in range(len(if00)):
    if i<=t_p:
        n_w.append(1) #前面因为算移动平均，无法进行计算
    else:
        if position==0: #未开仓     
            if boll['gap'].ix[i-1]<=boll['upline'].ix[i-1] and boll['gap'].ix[i]>boll['upline'].ix[i]:#上穿上限
                n_w.append(n_w[i-1])
                cost=(if00[i]+if01[i])/le #成交本金
                gap_open=boll['gap'].ix[i] #初始价差
                position=1
            elif boll['gap'].ix[i-1]>=boll['downline'].ix[i-1] and boll['gap'].ix[i]<boll['downline'].ix[i]:#下穿下限
                n_w.append(n_w[i-1])
                cost=(if00[i]+if01[i])/le
                gap_open=boll['gap'].ix[i]
                position=-1                            
            else:
                n_w.append(n_w[i-1])
        elif position==1: #开了正套
            #是否平仓
            if boll['gap'].ix[i-1]>=boll['mean'].ix[i-1] and boll['gap'].ix[i]<boll['mean'].ix[i]:#下穿均线平仓
                ret=(boll['gap'].ix[i-1]-boll['gap'].ix[i])/cost #价差变化/成本
                n_w.append((1+ret)*n_w[i-1])
                position=0
            else:
                ret=(gap_open-boll['gap'].ix[i])/cost
                n_w.append((1+ret)*n_w[i-1])
        else:
            #是否平仓
            if boll['gap'].ix[i-1]<=boll['mean'].ix[i-1] and boll['gap'].ix[i]>boll['mean'].ix[i]:#上穿均线平仓
                ret=(boll['gap'].ix[i]-boll['gap'].ix[i-1])/cost
                n_w.append((1+ret)*n_w[i-1])
                position=0
            else:
                ret=(boll['gap'].ix[i]-gap_open)/cost
                n_w.append((1+ret)*n_w[i-1])
                
fig4=plt.figure(4,figsize=(12,6))
plt.plot_date(date,n_w,'b-')
plt.title('净值图')

                
                
                
               
            
        
        
    
    
    
    




