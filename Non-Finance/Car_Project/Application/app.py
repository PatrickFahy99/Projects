import numpy as np
from flask import Flask, request, jsonify, render_template
import flask
import pickle


def change_input(make, year, typ, miles, litres, bhp, transmission, fuel, owners=2, ULEZ='No', model=''):
    
    import pandas as pd
    
    df = pd.DataFrame()
    df.at[0,'Owners'] = float(owners)
    df.at[0,'ULEZ'] = 1 if ULEZ=='Yes' else 0
    df.at[0,'Make_Audi'] = 1 if make=='Audi' else 0
    df.at[0,'Make_Bmw'] = 1 if make=='BMW' else 0
    df.at[0,'Make_Citroen'] = 1 if make=='Citroen' else 0
    df.at[0,'Make_Fiat'] = 1 if make=='Fiat' else 0
    df.at[0,'Make_Ford'] = 1 if make=='Ford' else 0
    df.at[0,'Make_Honda'] = 1 if make=='Honda' else 0
    df.at[0,'Make_Hyundai'] = 1 if make=='Hyundai' else 0
    df.at[0,'Make_Jaguar'] = 1 if make=='Jaguar' else 0
    df.at[0,'Make_Kia'] = 1 if make=='Kia' else 0
    df.at[0,'Make_Land Rover'] = 1 if make=='Land Rover' else 0
    df.at[0,'Make_Mazda'] = 1 if make=='Mazda' else 0
    df.at[0,'Make_Mercedes-Benz'] = 1 if make=='Mercedes-Benz' else 0
    df.at[0,'Make_Mini'] = 1 if make=='Mini' else 0
    df.at[0,'Make_Mitsubishi'] = 1 if make=='Mitsubishi' else 0
    df.at[0,'Make_Nissan'] = 1 if make=='Nissan' else 0
    df.at[0,'Make_Peugeot'] = 1 if make=='Peugeot' else 0
    df.at[0,'Make_Porsche'] = 1 if make=='Porsche' else 0
    df.at[0,'Make_Renault'] = 1 if make=='Renault' else 0
    df.at[0,'Make_Skoda'] = 1 if make=='Skoda' else 0
    df.at[0,'Make_Suzuki'] = 1 if make=='Suzuki' else 0
    df.at[0,'Make_Toyota'] = 1 if make=='Toyota' else 0
    df.at[0,'Make_Vauxhall'] = 1 if make=='Vauxhall' else 0
    df.at[0,'Make_Volkswagen'] = 1 if make=='Volkswagen' else 0
    df.at[0,'Make_Volvo'] = 1 if make=='Volvo' else 0
    df.at[0,'Type_Convertible'] = 1 if typ=='Convertible' else 0
    df.at[0,'Type_Coupe'] = 1 if typ=='Coupe' else 0
    df.at[0,'Type_Estate'] = 1 if typ=='Estate' else 0
    df.at[0,'Type_Hatchback'] = 1 if typ=='Hatchback' else 0
    df.at[0,'Type_Limousine'] = 1 if typ=='Limousine' else 0
    df.at[0,'Type_MPV'] = 1 if typ=='MPV' else 0
    df.at[0,'Type_Pickup'] = 1 if typ=='Pickup' else 0
    df.at[0,'Type_SUV'] = 1 if typ=='SUV' else 0
    df.at[0,'Type_Saloon'] = 1 if typ=='Saloon' else 0
    df.at[0,'Transmission_Automatic'] = 1 if transmission=='Automatic' else 0
    df.at[0,'Transmission_Manual'] = 1 if transmission=='Manual' else 0
    df.at[0,'Fuel_Diesel'] = 1 if fuel=='Diesel' else 0
    df.at[0,'Fuel_Hybrid'] = 1 if fuel=='Hybrid' else 0
    df.at[0,'Fuel_Petrol'] = 1 if fuel=='Petrol' else 0
    df.at[0,'mile_sc'] = ((miles**0.5)-218.1358)/90.4083
    df.at[0,'age_sc'] = (((2020-year)**0.5)-2.6427)/0.80541
    df.at[0,'lit_sc'] = (np.log(litres)-0.5680)/0.3133
    df.at[0,'bhp_sc'] = (np.log(bhp)-4.9177)/0.4109
    
    return df


def predict_price(df):
    
    import pickle

    
    model1 = pickle.load(open('/Users/patrickfahy99/Documents/GitHub/Projects/Non-Finance/Car_Project/car_model1', 'rb'))
    model2 = pickle.load(open('/Users/patrickfahy99/Documents/GitHub/Projects/Non-Finance/Car_Project/car_model2', 'rb'))
    pred1 = model1.predict(df)
    pred2 = model2.predict(df)

    pred = 0.5*pred1 + 0.5*pred2
    
    return pred


def get_output(pred):
    
    prediction = (pred * 40.0370 + 98.2822) ** 2
    
    return prediction


def predict_result(make, year, typ, miles, litres, bhp, transmission, fuel, owners=2, ULEZ='No', model=''):
    
    df = change_input(make, year, typ, miles, litres, bhp, transmission, fuel, owners=2, ULEZ='No', model='')
    pred = predict_price(df)
    prediction = get_output(pred)
    
    return prediction


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    info = [x for x in request.form.values()]
    
    make = info[0]
    year = int(info[1])
    typ = info[2]
    miles = float(info[3])
    litres = float(info[4])
    bhp = float(info[5])
    transmission = info[6]
    fuel = info[7]
    owners = float(info[8])
    ULEZ = info[9]

    prediction = predict_result(make, year, typ, miles, litres, bhp, transmission, fuel, owners, ULEZ)

    output = int(np.round(prediction))
    

    return render_template('index.html', prediction_text='Car value should (approximately) be £{}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    #prediction = model.predict([np.array(list(data.values()))])

    #output = prediction[0]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)







