import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BackTestUtilis import BackTestTools



def pairStrategy(data,costRecords, fund):
    gap = data[0] - data[1]
    times = 3  # 几倍标准差
    t_p = 20  # n天的移动平均
    initial = np.empty((4, len(data[0]),))
    initial[:] = np.NAN
    initial[0] = gap
    initial = initial.T
    boll = pd.DataFrame(initial, columns=["gap", "mean", "upline", "downline"])
    boll['mean'] = pd.rolling_mean(boll['gap'], t_p)  # 价差均线
    boll['upline'] = pd.rolling_mean(boll['gap'], t_p) + times * pd.rolling_std(boll['gap'], t_p)  # 上限
    boll['downline'] = pd.rolling_mean(boll['gap'], t_p) - times * pd.rolling_std(boll['gap'], t_p)  # 下限
    position = 0
    le = 2  # 杠杆
    for i in range(len(data[0])):
        if i <= t_p:
            costRecords.append(fund)  # 前面因为算移动平均，无法进行计算
        else:
            if position == 0:  # 未开仓
                if boll['gap'].ix[i - 1] <= boll['upline'].ix[i - 1] and boll['gap'].ix[i] > boll['upline'].ix[
                    i]:  # 上穿上限
                    costRecords.append(costRecords[i - 1])
                    cost = (data[0][i] + data[1][i]) / le  # 成交本金
                    gap_open = boll['gap'].ix[i]  # 初始价差
                    position = 1
                elif boll['gap'].ix[i - 1] >= boll['downline'].ix[i - 1] and boll['gap'].ix[i] < boll['downline'].ix[
                    i]:  # 下穿下限
                    costRecords.append(costRecords[i - 1])
                    cost = (data[0][i] + data[1][i]) / le
                    gap_open = boll['gap'].ix[i]
                    position = -1
                else:
                    costRecords.append(costRecords[i - 1])
            elif position == 1:  # 开了正套
                # 是否平仓
                if boll['gap'].ix[i - 1] >= boll['mean'].ix[i - 1] and boll['gap'].ix[i] < boll['mean'].ix[i]:  # 下穿均线平仓
                    ret = (gap_open - boll['gap'].ix[i]) / cost  # 价差变化/成本
                    costRecords.append((1 + ret) * costRecords[i - 1])
                    position = 0
                else:
                    ret = (gap_open - boll['gap'].ix[i]) / cost
                    costRecords.append((1 + ret) * costRecords[i - 1])
            else:
                # 是否平仓
                if boll['gap'].ix[i - 1] <= boll['mean'].ix[i - 1] and boll['gap'].ix[i] > boll['mean'].ix[i]:  # 上穿均线平仓
                    ret = (boll['gap'].ix[i] - gap_open) / cost
                    costRecords.append((1 + ret) * costRecords[i - 1])
                    position = 0
                else:
                    ret = (boll['gap'].ix[i] - gap_open) / cost
                    costRecords.append((1 + ret) * costRecords[i - 1])




if __name__ == "__main__":
    data = xlrd.open_workbook('dataday.xlsx')
    table = data.sheets()[0]
    date = table.col_values(0)  # 交易日期
    date = date[3:]
    if00 = table.col_values(5)  # 当月合约收盘价
    if00 = if00[3:]
    if01 = table.col_values(18)  # 下月合约收盘价
    if01 = if01[3:]
    dataset = np.array([if00, if01])
    test = BackTestTools(data=dataset, dateList=date, strategy=pairStrategy)
    test.runStrategy()
    test.staticPlot(['hs300'])

