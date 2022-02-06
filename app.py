from pyexpat import features
import numpy as np
from flask import Flask, render_template , request 
import pickle
import pandas as pd
from astropy.table import QTable
import astropy.units as u

app=Flask(__name__)
loaded_model = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/predict/',methods=['POST','GET'])
def predict():
     ''' For rendering results on HTML GUI'''
     
     df=pd.read_csv('D:/web dev/js-basics/TexasTurbine.csv')
     df.rename({
    'System power generated | (kW)': 'power',
    'Wind speed | (m/s)': 'wind_speed',
    'Wind direction | (deg)': 'wind_direction',
    'Pressure | (atm)': 'pressure',
    'Air temperature | (\'C)': 'temperature'
    }, inplace=True, axis=1)
  
     
     Steps = int(request.form.get('Steps'))*1
     data = df[['wind_speed']][-Steps:]
     print(type(loaded_model))
     prediction = loaded_model.predict(Steps,data)
     

     for i, val in enumerate(prediction):
      if val < 0:
        prediction[i] = val * -1
     #output = round(prediction[0])
     #steps_index = []
     #for i in range(1, (Steps+1)):
       #steps_index.append(df.index[-1] + pd.DateOffset(hours=i))
    # model_predict = pd.DataFrame(prediction, index=steps_index, columns=['next_' + str(Steps) + '_steps'])
     xstr = ""
     ct=0
     for e in prediction:
       if ct==(Steps-1):
         xstr+=str(round(e))
         ct+=1
       else: 
           xstr+=str(round(e)) + ","
           ct+=1

     #t = QTable([prediction])
     #print(xstr
    # output=round(prediction[0])

     return render_template('index.html', prediction_text='The predictions are  {} '.format(xstr))


if __name__=='__main__':
     app.run(port=1000,debug=True)   