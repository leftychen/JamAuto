from neural_network.BP_Neutral import BP_Netural
import sklearn.datasets as dst
import pandas as pd
import numpy as np
from mlxtend.evaluate import plot_decision_regions
import matplotlib.pyplot as plt
import sys
import pandas.io.data as web
import datetime
# GET Training DATA

start = (2013, 1, 1)
end = (2016, 1, 1)
start_date = datetime.datetime(start[0], start[1], start[2])
end_date = datetime.datetime(end[0], end[1], end[2])
try:
    Data = web.DataReader('^GSPC','yahoo',start_date, end_date)
except OSError as e:
    print("The ticker is not correct!")
    sys.exit()


# data conversion
Data_train = Data[0:-250]
Data_test = Data[-249:-1]# last 250 days to test the model
SP500_AdjClose = Data_train['Adj Close']
Netural_Work = BP_Netural() # call the object of Netural_Work
bestmodel = {} # to store the best fit model
minError = sys.maxsize
best_rolling_days = 0


for days in range(10,65, 5): # run with different rolling period days to check the best one 
    Y_SP500 = []
    SP500_returns = [SP500_AdjClose[days + x - 1] / SP500_AdjClose[x] - 1 for x \
                     in range(1,len(SP500_AdjClose) - days + 1 )]
    # Calculate the average return
    SP500_returns_forward = SP500_returns[1:-1]
    # Get the 1 - period forward return
    SP500_returns_forward = np.array(SP500_returns_forward)
    Y_SP500 = np.where(SP500_returns_forward > 0, 1, 0)
    # Change to dummy variable
    Avg_Std = pd.rolling_std(SP500_AdjClose.pct_change(), window=days)
    # Standard Deviation of returns in given period
    Avg_Std = Avg_Std.dropna()
    Matrix_input = np.column_stack((SP500_returns, Avg_Std.values))
    Matrix_input = Matrix_input[0:-2]
    model = Netural_Work.train(5, Matrix_input, Y_SP500)
    #Train the Data
    error = Netural_Work.modelloss(Netural_Work.model, Matrix_input, Y_SP500)
    #Record the Error and find the minimum error
    if error < minError:
        minError = error
        bestmodel = model
        best_rolling_days = days
    print("days:%s Errors: %s" %(days, error))

print("Best rolling days: %s" %best_rolling_days)

# Back Test Model 

Avg_Std_test = pd.rolling_std(Data_test['Adj Close'].pct_change(), window=best_rolling_days)
Avg_Std_test = Avg_Std_test.dropna()
SP500_test = [Data_test['Adj Close'][best_rolling_days + x - 1] / Data_test['Adj Close'][x] - 1 for x in \
              range(1,len(Data_test) - best_rolling_days + 1 )]
SP500_test_forward = SP500_test[1:-1]
SP500_test_forward = np.array(SP500_test_forward)
Y_SP500_test_forward = np.where(SP500_test_forward > 0, 1, 0)
Matrix_test = np.column_stack((SP500_test, Avg_Std_test.values))
Matrix_test = Matrix_test[0:-2]
predict_test = Netural_Work.predict(Matrix_test, model=bestmodel)
errors_test = np.abs(np.sum(predict_test - Y_SP500_test_forward))
ratio_mis_classified = errors_test/len(Y_SP500_test_forward)
print("%s points are mis-classified, predict accuracy is %s" %(errors_test, 1 - ratio_mis_classified))
