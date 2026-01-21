import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('coordinates.csv')

plt.plot(df['lat'], df['lon'])
plt.show()