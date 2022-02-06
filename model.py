import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
df=pd.read_csv('D:/web dev/js-basics/TexasTurbine.csv')
from datetime import datetime

def con_date(x):
    d = datetime.strptime(x, '%b %d, %I:%M %p')
    return(pd.to_datetime(d.replace(year=d.year + 120)))

df['time_stamp'] = df['Time stamp'].apply(lambda x : con_date(x))
df = df.set_index('time_stamp')

df.drop('Time stamp', axis=1, inplace=True)
df = df.asfreq('H')
df = df.fillna(method='ffill')

df.rename({
    'System power generated | (kW)': 'power',
    'Wind speed | (m/s)': 'wind_speed',
    'Wind direction | (deg)': 'wind_direction',
    'Pressure | (atm)': 'pressure',
    'Air temperature | (\'C)': 'temperature'
}, inplace=True, axis=1)

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima import auto_arima

train = df['power'][:7000]
test = df['power'][7000:]

from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
model_auto = auto_arima(df.power,
                        exogenous = df[['wind_speed']],
                        max_order = None,
                        max_p = 2,
                        max_q = 4,
                        max_d = 1,
                        max_P = 1, 
                        max_Q = 1, 
                        max_D = 1,
                        trend = 'ct')
print(model_auto.summary())

steps = 3
steps_index = []
for i in range(1, (steps+1)):
    steps_index.append(df.index[-1] + pd.DateOffset(hours=i))

forecast = model_auto.predict(n_periods=steps, exogenous=df[['wind_speed']][-steps:])
for i, val in enumerate(forecast):
    if val < 0:
        forecast[i] = val * -1

model_predict = pd.DataFrame(forecast, index=steps_index, columns=['next_' + str(steps) + '_steps'])
print(model_predict)
for i in model_predict['next_24_steps']:
  print(i)

#pickle.dump(forecast,open('model.pkl','wb'))
#loaded_model=pickle.load(open('model.pkl','rb'))  
