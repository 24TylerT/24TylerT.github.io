import pandas as pd
import matplotlib.pyplot as plt

s = pd.Series([1, 2, 3])
fig, ax = plt.subplots()
s.plot.bar()
print("hi");
fig.savefig('my_plot.png')