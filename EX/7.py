import pandas as pd
import matplotlib.pyplot as plt

data = [[500,450,520,610],[690,700,820,900],[1100,1030,1200,1380],[1500,1650,1700,1850],[1990,2020,2300,1420],[1020,1600,2200,2550]]
clm = ['1분기','2분기','3분기','4분기']
idex = [2015,2016,2017,2018,2019,2020]
df1 = pd.DataFrame(data,idex,clm)
df1.to_csv('/Users/nyul/data.csv',header=False,encoding='utf-8')
print(df1)



y=[]
df = pd.read_csv('/Users/nyul/data.csv',encoding = 'utf-8-sig',header=True)
for row in df.iterrows():
    y.append(row[1].values)

x= range(len(y[0]))
xLabel = ['firts','second','third','fourth']
yLabel = ['blue','orange','green','red','purple','brown']

for i in range(len(yLabel)):
    plt.plot(x, y[i], color=yLabel[i])

plt.title("2015~2020 Quarterly sales")
plt.xlabel('Quarters')
plt.ylabel('sales')
plt.xticks(x,xLabel,fontsize=10)
plt.legend(yLabel,loc='upper left')
plt.show()
