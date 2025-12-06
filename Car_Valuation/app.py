import streamlit as st
import pandas as pd 
import numpy as np
import xgboost as xgb
import json 
import os

# Configuration
st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")
model_path = os.path.join(current_dir, "xgb_car_price_model.json")
columns_path = os.path.join(current_dir, "model_columns.json")
data_path = os.path.join(current_dir, "cars_clean.csv")

# Load resources
@st.cache_resource
def load_resources():
    # load model
    model = xgb.XGBRegressor()
    model.load_model(model_path)
    
    # load column names
    with open(columns_path, "r") as f:
        model_columns = json.load(f)
    
    # load data
    df = pd.read_csv(data_path)

    return model, model_columns, df

model, model_columns, df = load_resources()

# user interface
st.title("Car Price Prediction")
st.write("Enter the features of the car and click on predict to get the price")

col1, col2 = st.columns(2)

with col1:
    make = st.selectbox("Make", sorted(df['Make'].unique()))

    availabe_models = sorted(df[df['Make'] == make]['model'].unique())
    car_model = st.selectbox("Model", availabe_models)

    year = st.number_input("Year", min_value=1900, max_value=2025, value=2025)
    mileage = st.number_input("Mileage", min_value=0, max_value=1000000, value=10000)

with col2:
    transmission = st.selectbox("Transmission", sorted(df['transmission'].unique()))
    fuel_type = st.selectbox("Fuel Type", sorted(df['fuelType'].unique()))

    engine_size = st.number_input("Engine Size", min_value=0.0, max_value=8.0, value=1.0, step=0.1)
    mpg = st.number_input("MPG", min_value=0, value=50)
    tax = st.number_input("Tax", min_value=0, value=150)

if st.button("Predict", type="primary"):
   
    input_data = {
        'year': year,
        'mileage': mileage,
        'fuel_type': fuel_type,
        'engine_size': engine_size,
        'mpg': mpg,
        'tax': tax,
        f'Make_{make}': 1,
        f'Model_{car_model}': 1,
        f'transmission_{transmission}': 1,
        f'fuel_type_{fuel_type}': 1,
    }    
    
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0

    for col, val in input_data.items():
        if col in input_df.columns:
            input_df.at[0, col] = val

    try:
        perdiction_log = model.predict(input_df)
        price_gbp = np.expm1(perdiction_log[0])
        price_pln = price_gbp * 4.85

        st.success(f"Predicted Price: {price_pln:.2f} PLN")

    except Exception as e:
        st.error(f"Error: {str(e)}")