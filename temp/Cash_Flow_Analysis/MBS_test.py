import numpy as np
from  MBS import MBS
import matplotlib.pyplot as plt

AA = MBS(0.007916 * 12, 100000000, 0.09, 355)
smmrate = AA.SMM(PSA = 150)
d = AA.CashFlowTable()
print(d.head(n=355))
plt.plot(d['Interest'])
plt.show()
