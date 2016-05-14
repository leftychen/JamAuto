
import numpy as np
import pandas as pd
class MBS:
    def __init__(self, PTRate, balance, WAC, WAM, Seasoning = 5):
        self.PTRate = PTRate
        self.balance = balance
        self.WAC = WAC
        self.WAM = WAM
        self.cpRate = 0.06
        self.smmRate = np.ones((self.WAM,1))
        self.Seasoning = Seasoning

    def SMM(self,PSA = 100, CPR = 0):
        # Calculate Single month mortality using PSA
        if CPR is not 0:
            self.cpRate = CPR
        for y in range(self.WAM):
            cpRate_temp = PSA/100 * ((y+ 1 + self.Seasoning)/30) * self.cpRate
            smmRate_temp = 1 - np.power((1 - cpRate_temp),1/12)
            self.smmRate[y] = smmRate_temp
            if(y == 30 - self.Seasoning - 1):
                self.smmRate[y:] = smmRate_temp
                break
        return self.smmRate

    def CashFlowTable(self):
        tempBalance = self.balance
        Balance = np.ones((self.WAM  ,1)) #Principal Balance
        Payment = np.ones((self.WAM  ,1)) # period Period
        Interest = np.ones((self.WAM  ,1))# Interest paid for current Period
        SchPrinPay = np.ones((self.WAM  ,1))# Schedule Principal paid
        PrePay = np.ones((self.WAM  ,1)) # Prepayment
        CF = np.ones((self.WAM ,1)) # Period Cash Flow
        PrinPaid = np.ones((self.WAM ,1)) # Actually Princial Paid
        Balance[0] = self.balance

        for y in range(self.WAM - 1):
            tempPay = self.__getpayment(tempBalance,y)
            Payment[y] = tempPay

            tempInerest = (self.PTRate/12) * tempBalance
            Interest[y] = tempInerest

            tempSchPrinPay = tempPay - (self.WAC/12) * tempBalance
            SchPrinPay[y] = tempSchPrinPay

            tempPrePay = self.smmRate[y] * (tempBalance - tempSchPrinPay)
            PrePay[y] = tempPrePay

            tempCF = tempPrePay + tempSchPrinPay + tempInerest
            CF[y] = tempCF

            tempBalance = tempBalance - tempSchPrinPay - tempPrePay
            Balance[y+1] = tempBalance

            tempPrinPaid = tempSchPrinPay + tempPrePay
            PrinPaid[y] = tempPrinPaid
        SchPrinPay[-1] = Balance[-1]
        Interest[-1] = (self.PTRate/12) * Balance[-1]
        Payment[-1] = SchPrinPay[-1] + (self.WAC/12) * Balance[-1]
        PrePay[-1] = 0
        PrinPaid[-1] = Balance[-1]
        CF[-1] = Interest[-1] + PrePay[-1] + SchPrinPay[-1]
        CFdic = np.concatenate((Balance,Interest,Payment,SchPrinPay,self.smmRate,\
                                PrePay,PrinPaid,CF), axis = 1)
        legend = ['Balance','Interest','Payment', 'SchPrin', 'SMM', 'PrePaid', 'PrinPaid', 'CF']

        Re = pd.DataFrame(data=CFdic, columns=legend)
        return Re

    def __getpayment(self,balance, y):
        pow = np.power((1 + self.PTRate/12),self.WAM - y)
        dst = (1 - 1/pow)/(self.WAC/12)
        pay = balance / dst
        return pay
