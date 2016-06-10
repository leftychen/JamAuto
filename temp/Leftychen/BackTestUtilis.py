import numpy as np
import matplotlib.pyplot as plt

class BackTestTools:
    # Initialized
    def __init__(self, data, dateList, strategy = None, Model = None):
        if strategy == None and Model == None:
            raise KeyError("Strategy and Model cannot both be Null ")
        self.__data = data  # Data for BackTest
        self.__dateList = dateList # Datestamp for backtest
        self.__initFund = 1000000 # initial fund for backtest
        self.__strategy = strategy # abstract func needs to be overided
        self.__Model = Model # abstract func that needs to be overided
        self.__costRecords = []

    def __strategy(self,data,date, **args):
        pass

    def __Model(self, **args):
        pass
    #re-set the initial Fund
    def setInitialFund(self,fund):
        self.__initFund = fund
    # run your Strategy
    def runStrategy(self):
        self.__strategy(self.__data, self.__costRecords,self.__initFund)
        self.__costRecords = np.array(self.__costRecords)
        self.__profit = (self.__costRecords[1:len(self.__costRecords)] \
                            - self.__costRecords[0:-1]) / self.__costRecords[1:len(self.__costRecords)]
        self.__cumProfit = np.cumsum(self.__profit)
        print("Total Days of investing: %s" %len(self.__dateList))
        print("Initial Fund : %s"  %self.__initFund)
        print("Final Fund Value: %s" %self.__costRecords[-1])
        print("Final return: %s" %self.__cumProfit[-1])
        print("Average Daily Return: %s" %np.mean(self.__profit))
        print("BackTest finish,please run plot to check your result...")

    # Plot static graph
    def staticPlot(self, legend):
        plt.plot_date(self.__dateList[1:len(self.__dateList)], self.__cumProfit, 'b-')

        plt.title("Back Test Result")
        plt.xlabel("date")
        plt.ylabel("Profit Ratio")
        plt.legend(legend, loc="upper left")
        plt.show()








